import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from agent.tools import LogisticsToolkit
from agent.prompts import SYNAPSE_SYSTEM_PROMPT, REACT_PROMPT_TEMPLATE
from utils.logger import get_logger

logger = get_logger(__name__)

class SynapseAgent:
    """
    Autonomous AI coordinator for last-mile delivery disruptions.
    Uses ReAct pattern (Reasoning + Acting) with LangChain framework.
    """
    
    def __init__(self):
        """Initialize the Synapse agent with tools and LLM"""
        self.llm = self._initialize_llm()
        self.toolkit = LogisticsToolkit()
        self.tools = self._setup_tools()
        self.agent_executor = self._create_agent_executor()
        
        logger.info("Synapse Agent initialized successfully")
    
    def _initialize_llm(self):
        """Initialize the language model - try OpenAI first, fallback to Gemini"""
        # Try OpenAI first
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                # The newest OpenAI model is "gpt-5" which was released August 7, 2025.
                # Do not change this unless explicitly requested by the user
                return ChatOpenAI(
                    model="gpt-5",
                    api_key=openai_key,
                    temperature=0.1,  # Low temperature for consistent reasoning
                    max_completion_tokens=2000
                )
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}. Trying Gemini...")
        
        # Fallback to Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            try:
                # Note that the newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
                # do not change this unless explicitly requested by the user
                return ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    google_api_key=gemini_key,
                    temperature=0.1,
                    max_output_tokens=2000
                )
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        
        raise ValueError("Either OPENAI_API_KEY or GEMINI_API_KEY environment variable is required")
    
    def _setup_tools(self) -> List[Tool]:
        """Setup all available logistics tools"""
        tools = []
        
        # Traffic and routing tools
        tools.append(Tool(
            name="check_traffic",
            description="Check current traffic conditions, incidents, and estimated delays on specific routes. Input: route description or coordinates",
            func=self.toolkit.check_traffic
        ))
        
        tools.append(Tool(
            name="calculate_alternative_route",
            description="Find alternative routes when primary route is blocked. Input: origin, destination, avoid_areas",
            func=self.toolkit.calculate_alternative_route
        ))
        
        # Merchant and restaurant tools
        tools.append(Tool(
            name="get_merchant_status",
            description="Check merchant availability, prep times, and current status. Input: merchant_id or merchant_name",
            func=self.toolkit.get_merchant_status
        ))
        
        tools.append(Tool(
            name="find_nearby_alternatives",
            description="Find nearby alternative merchants or services when original is unavailable. Input: location, service_type, requirements",
            func=self.toolkit.find_nearby_alternatives
        ))
        
        # Customer communication tools
        tools.append(Tool(
            name="notify_customer",
            description="Send notifications to customers about delays, changes, or updates. Input: customer_id, message_type, details",
            func=self.toolkit.notify_customer
        ))
        
        tools.append(Tool(
            name="contact_recipient",
            description="Contact delivery recipient via chat, call, or SMS. Input: recipient_contact, message_type, urgency",
            func=self.toolkit.contact_recipient
        ))
        
        # Driver and delivery tools
        tools.append(Tool(
            name="reroute_driver",
            description="Reassign or reroute driver to optimize efficiency. Input: driver_id, new_assignment, priority",
            func=self.toolkit.reroute_driver
        ))
        
        tools.append(Tool(
            name="find_secure_location",
            description="Find secure drop-off locations like lockers, concierge, or safe spots. Input: address, package_type, security_level",
            func=self.toolkit.find_secure_location
        ))
        
        # Resolution and compensation tools
        tools.append(Tool(
            name="initiate_refund",
            description="Process customer refunds or compensation for issues. Input: order_id, refund_type, amount, reason",
            func=self.toolkit.initiate_refund
        ))
        
        tools.append(Tool(
            name="escalate_to_support",
            description="Escalate complex issues to human support team. Input: issue_details, priority_level, customer_info",
            func=self.toolkit.escalate_to_support
        ))
        
        return tools
    
    def _create_agent_executor(self) -> AgentExecutor:
        """Create the ReAct agent executor"""
        # Create the ReAct prompt
        prompt = PromptTemplate(
            template=REACT_PROMPT_TEMPLATE,
            input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
        )
        
        # Create the agent
        agent = create_react_agent(self.llm, self.tools, prompt)
        
        # Create and return the executor
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            early_stopping_method="generate",
            handle_parsing_errors=True
        )
    
    def resolve_disruption(self, scenario: str) -> Dict[str, Any]:
        """
        Main method to resolve a disruption scenario
        
        Args:
            scenario: Natural language description of the disruption
            
        Returns:
            Dict containing resolution results and reasoning chain
        """
        logger.info(f"Starting disruption resolution for scenario: {scenario[:100]}...")
        
        start_time = time.time()
        reasoning_steps = []
        action_trace = []
        
        try:
            # Prepare the input with system context
            enhanced_input = f"""
            {SYNAPSE_SYSTEM_PROMPT}
            
            DISRUPTION SCENARIO:
            {scenario}
            
            Please analyze this scenario and provide a step-by-step resolution plan.
            Use the available tools to gather information and execute actions.
            Show your reasoning at each step.
            """
            
            # Execute the agent
            result = self.agent_executor.invoke({
                "input": enhanced_input
            })
            
            # Extract reasoning from the agent's intermediate steps
            if hasattr(result, 'intermediate_steps'):
                for step in result['intermediate_steps']:
                    if isinstance(step[0], AgentAction):
                        action = step[0]
                        observation = step[1]
                        
                        reasoning_steps.append({
                            "thought": action.log.split('\n')[0] if action.log else "Thinking...",
                            "reasoning": action.log,
                            "tool_used": action.tool,
                            "tool_input": action.tool_input,
                            "observation": str(observation),
                            "tool_output": self._parse_tool_output(observation)
                        })
                        
                        action_trace.append({
                            "step": len(action_trace) + 1,
                            "timestamp": datetime.now().isoformat(),
                            "action": action.tool,
                            "input": str(action.tool_input),
                            "output": str(observation)
                        })
            
            execution_time = time.time() - start_time
            
            # Determine if resolution was successful
            final_output = result.get('output', '')
            resolution_success = self._evaluate_resolution_success(final_output, reasoning_steps)
            
            resolution_result = {
                "resolution_success": resolution_success,
                "final_solution": final_output,
                "reasoning_steps": reasoning_steps,
                "action_trace": action_trace,
                "execution_time": execution_time,
                "tools_used": len(set(step.get('tool_used', '') for step in reasoning_steps)),
                "total_steps": len(reasoning_steps)
            }
            
            logger.info(f"Disruption resolution completed. Success: {resolution_success}, Steps: {len(reasoning_steps)}")
            return resolution_result
            
        except Exception as e:
            logger.error(f"Error during disruption resolution: {str(e)}")
            return {
                "resolution_success": False,
                "final_solution": f"Resolution failed due to error: {str(e)}",
                "reasoning_steps": reasoning_steps,
                "action_trace": action_trace,
                "execution_time": time.time() - start_time,
                "error": str(e)
            }
    
    def _parse_tool_output(self, observation: Any) -> Dict:
        """Parse tool output into structured format"""
        try:
            if isinstance(observation, str):
                # Try to parse as JSON
                try:
                    return json.loads(observation)
                except json.JSONDecodeError:
                    return {"output": observation}
            elif isinstance(observation, dict):
                return observation
            else:
                return {"output": str(observation)}
        except Exception:
            return {"output": str(observation)}
    
    def _evaluate_resolution_success(self, final_output: str, reasoning_steps: List[Dict]) -> bool:
        """
        Evaluate whether the resolution was successful based on output and steps taken
        """
        if not final_output:
            return False
        
        # Check for success indicators in the output
        success_indicators = [
            "resolved", "solution", "plan", "notified", "rerouted", 
            "refund", "alternative", "contacted", "completed"
        ]
        
        failure_indicators = [
            "failed", "unable", "cannot", "error", "impossible"
        ]
        
        output_lower = final_output.lower()
        
        # Count success vs failure indicators
        success_count = sum(1 for indicator in success_indicators if indicator in output_lower)
        failure_count = sum(1 for indicator in failure_indicators if indicator in output_lower)
        
        # Check if tools were actually used
        tools_used = len([step for step in reasoning_steps if step.get('tool_used')])
        
        # Resolution is successful if:
        # 1. More success indicators than failure indicators
        # 2. At least some tools were used
        # 3. Output is substantial (not just an error message)
        return (
            success_count > failure_count and 
            tools_used > 0 and 
            len(final_output.strip()) > 50
        )
    
    def get_available_tools(self) -> List[Dict[str, str]]:
        """Get list of available tools with descriptions"""
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools
        ]
