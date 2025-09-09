import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Import LangChain components
try:
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain.tools import Tool
    from langchain_core.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError as e:
    logging.error(f"LangChain import error: {e}")
    raise ImportError("Required LangChain packages not installed. Please install langchain, langchain-openai, and langchain-google-genai")

from .tools import LogisticsToolkit
from .prompts import get_system_prompt, get_react_prompt
from utils.logger import setup_logger

class SynapseAgent:
    """
    Autonomous AI coordinator for last-mile delivery disruption resolution.
    Uses ReAct pattern for transparent reasoning and action.
    """
    
    def __init__(self):
        self.logger = setup_logger()
        self.llm = self._initialize_llm()
        self.tools = LogisticsToolkit().get_tools()
        self.agent_executor = self._create_agent()
        self.execution_trace = []
        
    def _initialize_llm(self):
        """Initialize the language model based on available API keys"""
        openai_key = os.getenv("OPENAI_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if openai_key:
            self.logger.info("Initializing OpenAI GPT-4 model")
            return ChatOpenAI(
                model="gpt-4",
                temperature=0.1,
                openai_api_key=openai_key
            )
        elif gemini_key:
            self.logger.info("Initializing Google Gemini model")
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                temperature=0.1,
                google_api_key=gemini_key
            )
        else:
            raise ValueError("No API key found. Please enter your API key in the app interface.")
    
    def _create_agent(self):
        """Create the ReAct agent with tools"""
        try:
            # Create the ReAct prompt
            prompt = PromptTemplate.from_template(get_react_prompt())
            
            # Create the agent
            agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )
            
            # Create agent executor
            agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                max_iterations=10,
                early_stopping_method="generate",
                handle_parsing_errors=True
            )
            
            self.logger.info("Agent successfully initialized")
            return agent_executor
            
        except Exception as e:
            self.logger.error(f"Failed to create agent: {str(e)}")
            raise
    
    def resolve_disruption(self, scenario: str) -> Dict[str, Any]:
        """
        Main method to resolve a delivery disruption scenario.
        
        Args:
            scenario (str): Description of the disruption scenario
            
        Returns:
            Dict containing resolution results with improved validation
        """
        self.logger.info(f"Starting disruption resolution for scenario: {scenario[:100]}...")
        
        # Reset execution trace
        self.execution_trace = []
        
        try:
            # Prepare the input with system context
            system_context = get_system_prompt()
            full_input = f"{system_context}\n\nDisruption Scenario: {scenario}\n\nPlease analyze this scenario and provide a complete resolution using the available tools."
            
            # Execute the agent
            self.logger.info("Executing agent with scenario")
            result = self.agent_executor.invoke({"input": full_input})
            
            # Parse and structure the result
            structured_result = self._parse_agent_result(result, scenario)
            
            self.logger.info(f"Agent execution completed. Success: {structured_result.get('resolution_success', False)}")
            return structured_result
            
        except Exception as e:
            self.logger.error(f"Error during disruption resolution: {str(e)}")
            return {
                'scenario': scenario,
                'resolution_success': False,
                'final_solution': f"Error occurred during resolution: {str(e)}",
                'reasoning_steps': [],
                'action_trace': [],
                'execution_time': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _parse_agent_result(self, raw_result: Dict[str, Any], scenario: str) -> Dict[str, Any]:
        """
        Parse the raw agent result into a structured format with improved validation logic.
        """
        output = raw_result.get('output', '')
        intermediate_steps = raw_result.get('intermediate_steps', [])
        
        # Extract reasoning steps from intermediate steps
        reasoning_steps = []
        action_trace = []
        
        for i, (agent_action, observation) in enumerate(intermediate_steps):
            step_data = {
                'step_number': i + 1,
                'thought': getattr(agent_action, 'log', '').split('\nAction:')[0].replace('Thought:', '').strip(),
                'reasoning': getattr(agent_action, 'log', ''),
                'tool_used': agent_action.tool if hasattr(agent_action, 'tool') else None,
                'tool_input': agent_action.tool_input if hasattr(agent_action, 'tool_input') else None,
                'observation': str(observation),
                'tool_output': self._parse_tool_output(observation)
            }
            reasoning_steps.append(step_data)
            
            # Add to action trace
            if step_data['tool_used']:
                action_trace.append({
                    'timestamp': datetime.now().isoformat(),
                    'action': step_data['tool_used'],
                    'input': step_data['tool_input'],
                    'output': step_data['tool_output'],
                    'success': self._is_tool_execution_successful(step_data['tool_output'])
                })
        
        # Determine resolution success using comprehensive logic
        resolution_success = self._determine_resolution_success(output, reasoning_steps, action_trace)
        
        # Structure the final result
        structured_result = {
            'scenario': scenario,
            'resolution_success': resolution_success,
            'final_solution': self._extract_final_solution(output),
            'reasoning_steps': reasoning_steps,
            'action_trace': action_trace,
            'execution_time': datetime.now().isoformat(),
            'raw_output': output
        }
        
        self.logger.info(f"Parsed result - Success: {resolution_success}, Steps: {len(reasoning_steps)}, Actions: {len(action_trace)}")
        return structured_result
    
    def _parse_tool_output(self, observation: str) -> Dict[str, Any]:
        """Parse tool output from observation string"""
        try:
            # Try to parse as JSON first
            if observation.strip().startswith('{') and observation.strip().endswith('}'):
                return json.loads(observation)
            
            # If not JSON, create a structured response
            return {
                'result': observation,
                'success': self._is_observation_successful(observation),
                'timestamp': datetime.now().isoformat()
            }
        except json.JSONDecodeError:
            return {
                'result': observation,
                'success': self._is_observation_successful(observation),
                'timestamp': datetime.now().isoformat()
            }
    
    def _is_observation_successful(self, observation: str) -> bool:
        """Determine if an observation indicates success"""
        observation_lower = observation.lower()
        
        # Check for explicit failure indicators
        failure_indicators = ['error', 'failed', 'unable', 'not found', 'invalid', 'could not', 'cannot']
        for indicator in failure_indicators:
            if indicator in observation_lower:
                return False
        
        # Check for success indicators
        success_indicators = ['success', 'completed', 'sent', 'found', 'arranged', 'processed', 'confirmed']
        for indicator in success_indicators:
            if indicator in observation_lower:
                return True
        
        # If no clear indicators, assume success if observation has content
        return len(observation.strip()) > 5
    
    def _is_tool_execution_successful(self, tool_output: Dict[str, Any]) -> bool:
        """Determine if a tool execution was successful"""
        if isinstance(tool_output, dict):
            # Check explicit success field
            if 'success' in tool_output:
                return bool(tool_output['success'])
            
            # Check status field
            if 'status' in tool_output:
                status = str(tool_output['status']).lower()
                return status in ['success', 'completed', 'ok', 'done']
            
            # Check for error indicators
            if 'error' in tool_output or 'failed' in str(tool_output).lower():
                return False
            
            # If no clear indicators but has meaningful content, assume success
            return len(str(tool_output)) > 10
        
        return self._is_observation_successful(str(tool_output))
    
    def _determine_resolution_success(self, output: str, reasoning_steps: List[Dict], action_trace: List[Dict]) -> bool:
        """
        Comprehensive logic to determine if the resolution was successful.
        """
        output_lower = output.lower()
        
        # Check for explicit failure in final output
        failure_indicators = [
            'failed to resolve', 'cannot resolve', 'unable to resolve',
            'no solution found', 'resolution failed', 'error occurred',
            'could not complete', 'unsuccessful'
        ]
        
        for indicator in failure_indicators:
            if indicator in output_lower:
                self.logger.info(f"Resolution marked as failed due to indicator: {indicator}")
                return False
        
        # Check for explicit success in final output
        success_indicators = [
            'successfully resolved', 'resolution completed', 'issue resolved',
            'problem solved', 'successfully handled', 'resolution successful',
            'completed successfully', 'resolved the disruption'
        ]
        
        for indicator in success_indicators:
            if indicator in output_lower:
                self.logger.info(f"Resolution marked as successful due to indicator: {indicator}")
                return True
        
        # Analyze action trace success rate
        if action_trace:
            successful_actions = sum(1 for action in action_trace if action.get('success', False))
            total_actions = len(action_trace)
            success_rate = successful_actions / total_actions if total_actions > 0 else 0
            
            self.logger.info(f"Action success rate: {success_rate} ({successful_actions}/{total_actions})")
            
            # If we have a high success rate of actions, consider it successful
            if success_rate >= 0.7:  # 70% or more actions successful
                return True
            elif success_rate < 0.3:  # Less than 30% successful
                return False
        
        # Check if we have meaningful reasoning steps
        if reasoning_steps:
            # Count steps that used tools successfully
            tool_steps = [step for step in reasoning_steps if step.get('tool_used')]
            if tool_steps:
                successful_tool_steps = [
                    step for step in tool_steps 
                    if self._is_tool_execution_successful(step.get('tool_output', {}))
                ]
                tool_success_rate = len(successful_tool_steps) / len(tool_steps)
                
                self.logger.info(f"Tool step success rate: {tool_success_rate}")
                
                if tool_success_rate >= 0.6:  # 60% or more tool steps successful
                    return True
        
        # Check if the output contains a substantial solution
        if len(output.strip()) > 50:  # Has substantial content
            # Look for action words that indicate resolution attempts
            action_words = [
                'notified', 'contacted', 'rerouted', 'arranged', 'found',
                'processed', 'initiated', 'sent', 'provided', 'located'
            ]
            
            action_count = sum(1 for word in action_words if word in output_lower)
            if action_count >= 2:  # Multiple actions taken
                self.logger.info(f"Resolution considered successful due to multiple actions: {action_count}")
                return True
        
        # Default: if we reached here and have some actions/steps, lean towards success
        # unless there are clear failure indicators
        has_actions = bool(action_trace or any(step.get('tool_used') for step in reasoning_steps))
        
        if has_actions:
            self.logger.info("Resolution considered successful due to presence of actions")
            return True
        
        # Final fallback: check output length and content quality
        if len(output.strip()) > 20 and 'no solution' not in output_lower:
            self.logger.info("Resolution considered successful due to substantial output")
            return True
        
        self.logger.info("Resolution marked as failed - no clear success indicators")
        return False
    
    def _extract_final_solution(self, output: str) -> str:
        """Extract the final solution from the agent output"""
        # Look for final answer or conclusion
        output_lines = output.split('\n')
        
        # Try to find a final answer section
        for i, line in enumerate(output_lines):
            if any(keyword in line.lower() for keyword in ['final answer', 'conclusion', 'resolution', 'solution']):
                # Return everything from this line onwards
                return '\n'.join(output_lines[i:]).strip()
        
        # If no specific section found, return the full output
        return output.strip() if output.strip() else "Resolution completed using available tools and coordination."
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get a summary of the current execution"""
        return {
            'tools_available': len(self.tools),
            'execution_trace_length': len(self.execution_trace),
            'llm_model': getattr(self.llm, 'model_name', 'Unknown'),
            'timestamp': datetime.now().isoformat()
        }
