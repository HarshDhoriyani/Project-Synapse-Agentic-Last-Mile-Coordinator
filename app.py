import streamlit as st
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agent.synapse_agent import SynapseAgent
from scenarios.test_scenarios import get_sample_scenarios
from utils.logger import setup_logger
import os

# Page config
st.set_page_config(
    page_title="Project Synapse - Agentic Last-Mile Coordinator",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize logger
logger = setup_logger()

# Initialize session state
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = SynapseAgent()
        st.session_state.execution_history = []
        st.session_state.performance_metrics = {
            'total_scenarios': 0,
            'successful_resolutions': 0,
            'average_response_time': 0,
            'tools_used': {}
        }
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        st.stop()

def display_header():
    st.title("🚚 Project Synapse")
    st.subheader("Agentic Last-Mile Coordinator")
    st.markdown("""
    An autonomous AI coordinator that resolves last-mile delivery disruptions using 
    intelligent reasoning and tool execution.
    """)
    
    # API Key Input Section
    st.markdown("### 🔑 API Key Configuration")
    
    # Check if API key is already in session state
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    
    # API Key input box
    api_key_input = st.text_input(
        "Enter your Google Gemini API Key:",
        type="password",
        value=st.session_state.api_key,
        placeholder="Paste your Gemini API key here (starts with AIzaSy...)",
        help="Get a free API key from Google AI Studio: https://aistudio.google.com/"
    )
    
    # Update session state if key is entered
    if api_key_input and api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.rerun()
    
    # Display API key status
    if st.session_state.api_key and len(st.session_state.api_key) > 30:
        st.success("✅ Gemini API Key configured and ready!")
        st.info("ℹ️ Using Google Gemini as the AI provider")
        
        # Store API key in environment for agent to use
        os.environ["GEMINI_API_KEY"] = st.session_state.api_key
        
    elif st.session_state.api_key:
        st.warning("⚠️ API key seems too short. Please check your key.")
    else:
        st.error("❌ Please enter your Gemini API Key to continue")
        st.markdown("""
        **To get a free Gemini API key:**
        1. Go to [Google AI Studio](https://aistudio.google.com/)
        2. Sign in with your Google account
        3. Click "Get API Key" and create a new key
        4. Copy and paste it in the box above
        
        Gemini offers free usage up to certain limits, perfect for testing this application!
        """)
        st.stop()

def display_metrics_dashboard():
    st.header("📊 Performance Metrics")
    
    metrics = st.session_state.performance_metrics
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Scenarios",
            metrics['total_scenarios']
        )
    
    with col2:
        success_rate = (metrics['successful_resolutions'] / max(metrics['total_scenarios'], 1)) * 100
        st.metric(
            "Success Rate",
            f"{success_rate:.1f}%"
        )
    
    with col3:
        st.metric(
            "Avg Response Time",
            f"{metrics['average_response_time']:.2f}s"
        )
    
    with col4:
        st.metric(
            "Tools Used",
            len(metrics['tools_used'])
        )
    
    # Tools usage chart
    if metrics['tools_used']:
        st.subheader("Tools Usage Distribution")
        tools_df = pd.DataFrame(
            data=list(metrics['tools_used'].items()),
            columns=['Tool', 'Usage Count']
        )
        fig = px.bar(tools_df, x='Tool', y='Usage Count', 
                    title="Tool Usage Frequency")
        st.plotly_chart(fig, use_container_width=True)

def display_scenario_input():
    st.header("🎯 Disruption Scenario Input")
    
    # Sample scenarios selector
    sample_scenarios = get_sample_scenarios()
    scenario_names = list(sample_scenarios.keys())
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_scenario = st.selectbox(
            "Choose a sample scenario or enter custom:",
            ["Custom"] + scenario_names
        )
    
    with col2:
        if st.button("Load Sample", type="secondary"):
            if selected_scenario != "Custom":
                st.session_state.scenario_text = sample_scenarios[selected_scenario]
                st.rerun()
    
    # Text input for scenario
    scenario_text = st.text_area(
        "Describe the disruption scenario:",
        value=st.session_state.get('scenario_text', ''),
        height=150,
        placeholder="Example: A GrabFood order is delayed because the restaurant is overcrowded with a 40-minute prep time..."
    )
    
    # Execution button
    col1, col2 = st.columns([1, 4])
    with col1:
        execute_button = st.button("🚀 Execute Resolution", type="primary")
    
    if execute_button and scenario_text.strip():
        st.session_state.current_scenario = scenario_text
        execute_scenario(scenario_text)
    elif execute_button:
        st.error("Please enter a disruption scenario.")

def execute_scenario(scenario_text):
    """Execute the scenario resolution with the agent"""
    st.header("🤖 Agent Execution")
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Start execution
        status_text.text("Initializing agent...")
        progress_bar.progress(10)
        
        # Execute the agent
        status_text.text("Agent analyzing scenario...")
        progress_bar.progress(30)
        
        start_time = datetime.now()
        result = st.session_state.agent.resolve_disruption(scenario_text)
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        progress_bar.progress(100)
        status_text.text("Execution completed!")
        
        # Update metrics
        update_metrics(result, execution_time)
        
        # Display results
        display_execution_results(result, execution_time)
        
    except Exception as e:
        st.error(f"Execution failed: {str(e)}")
        logger.error(f"Scenario execution failed: {str(e)}")

def update_metrics(result, execution_time):
    """Update performance metrics with improved validation"""
    metrics = st.session_state.performance_metrics
    
    metrics['total_scenarios'] += 1
    
    # Improved resolution success determination
    resolution_success = determine_resolution_success(result)
    logger.info(f"Resolution success determined as: {resolution_success}")
    
    if resolution_success:
        metrics['successful_resolutions'] += 1
    
    # Update average response time
    total_time = metrics['average_response_time'] * (metrics['total_scenarios'] - 1) + execution_time
    metrics['average_response_time'] = total_time / metrics['total_scenarios']
    
    # Update tools usage
    for step in result.get('reasoning_steps', []):
        tool_name = step.get('tool_used')
        if tool_name:
            metrics['tools_used'][tool_name] = metrics['tools_used'].get(tool_name, 0) + 1

def determine_resolution_success(result):
    """
    Improved logic to determine if a resolution was successful
    """
    # Check if explicit success flag is set
    if 'resolution_success' in result:
        explicit_success = result['resolution_success']
        if isinstance(explicit_success, bool):
            return explicit_success
        elif isinstance(explicit_success, str):
            return explicit_success.lower() in ['true', 'yes', 'successful', 'success']
    
    # Check final solution content
    final_solution = result.get('final_solution', '').lower()
    if not final_solution or final_solution == 'no solution provided':
        return False
    
    # Look for success indicators in the solution
    success_indicators = [
        'successfully', 'resolved', 'completed', 'arranged', 'notified',
        'rerouted', 'alternative found', 'refund processed', 'contacted',
        'secure location found', 'delivery confirmed'
    ]
    
    failure_indicators = [
        'failed', 'error', 'unable to', 'could not', 'cannot',
        'no solution', 'unresolved', 'unsuccessful'
    ]
    
    # Check for failure indicators first (they take precedence)
    for indicator in failure_indicators:
        if indicator in final_solution:
            return False
    
    # Check for success indicators
    for indicator in success_indicators:
        if indicator in final_solution:
            return True
    
    # Check reasoning steps for successful tool executions
    reasoning_steps = result.get('reasoning_steps', [])
    successful_actions = 0
    total_actions = 0
    
    for step in reasoning_steps:
        if step.get('tool_used'):
            total_actions += 1
            tool_output = step.get('tool_output', {})
            
            # Check if tool execution was successful
            if isinstance(tool_output, dict):
                if tool_output.get('success', False) or tool_output.get('status') == 'success':
                    successful_actions += 1
                elif 'error' not in tool_output and 'failed' not in str(tool_output).lower():
                    successful_actions += 1
    
    # If we have actions and most were successful, consider it a success
    if total_actions > 0:
        success_rate = successful_actions / total_actions
        return success_rate >= 0.5  # At least 50% of actions successful
    
    # If we have a solution but no clear indicators, default to success
    return len(final_solution.strip()) > 10  # Has substantial solution content

def display_execution_results(result, execution_time):
    """Display the execution results with improved validation"""
    st.success(f"✅ Execution completed in {execution_time:.2f} seconds")
    
    # Determine resolution success using improved logic
    resolution_success = determine_resolution_success(result)
    
    # Final resolution
    st.subheader("🎯 Final Resolution")
    resolution_status = "✅ Successful" if resolution_success else "❌ Failed"
    st.markdown(f"**Status:** {resolution_status}")
    
    final_solution = result.get('final_solution', 'No solution provided')
    st.markdown(f"**Solution:** {final_solution}")
    
    # Debug information
    with st.expander("🔍 Debug Information"):
        st.markdown("**Raw Result Data:**")
        st.json(result)
        st.markdown(f"**Resolution Success Determination:** {resolution_success}")
        if 'resolution_success' in result:
            st.markdown(f"**Original resolution_success value:** {result['resolution_success']} (type: {type(result['resolution_success'])})")
    
    # Chain of thought
    st.subheader("🧠 Chain of Thought Reasoning")
    
    reasoning_steps = result.get('reasoning_steps', [])
    if reasoning_steps:
        for i, step in enumerate(reasoning_steps, 1):
            with st.expander(f"Step {i}: {step.get('thought', 'Thinking...')}", expanded=i==1):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("**Reasoning:**")
                    st.write(step.get('reasoning', 'No reasoning provided'))
                    
                    if step.get('tool_used'):
                        st.markdown("**Tool Used:**")
                        st.code(step['tool_used'])
                
                with col2:
                    st.markdown("**Observation:**")
                    st.write(step.get('observation', 'No observation'))
                    
                    if step.get('tool_output'):
                        st.markdown("**Tool Output:**")
                        st.json(step['tool_output'])
                        
                        # Show tool success status
                        tool_output = step.get('tool_output', {})
                        if isinstance(tool_output, dict):
                            if 'success' in tool_output:
                                status = "✅ Success" if tool_output['success'] else "❌ Failed"
                                st.markdown(f"**Tool Status:** {status}")
    else:
        st.info("No reasoning steps recorded.")
    
    # Action trace
    st.subheader("📝 Action Trace")
    action_trace = result.get('action_trace', [])
    if action_trace:
        trace_df = pd.DataFrame(action_trace)
        st.dataframe(trace_df, use_container_width=True)
    
    # Save to history with corrected success status
    st.session_state.execution_history.append({
        'timestamp': datetime.now(),
        'scenario': st.session_state.get('current_scenario', ''),
        'result': {**result, 'resolution_success': resolution_success},  # Override with corrected status
        'execution_time': execution_time
    })

def display_history():
    """Display execution history"""
    st.header("📜 Execution History")
    
    if st.session_state.execution_history:
        for i, execution in enumerate(reversed(st.session_state.execution_history)):
            with st.expander(f"Execution {len(st.session_state.execution_history) - i} - {execution['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                st.markdown(f"**Scenario:** {execution['scenario'][:200]}...")
                success_icon = '✅' if execution['result'].get('resolution_success') else '❌'
                st.markdown(f"**Success:** {success_icon}")
                st.markdown(f"**Execution Time:** {execution['execution_time']:.2f}s")
                st.markdown(f"**Solution:** {execution['result'].get('final_solution', 'No solution')}")
    else:
        st.info("No execution history available.")

def main():
    """Main application function"""
    display_header()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        ["🎯 Scenario Resolution", "📊 Dashboard", "📜 History", "ℹ️ About"]
    )
    
    if page == "🎯 Scenario Resolution":
        display_scenario_input()
    elif page == "📊 Dashboard":
        display_metrics_dashboard()
    elif page == "📜 History":
        display_history()
    elif page == "ℹ️ About":
        display_about()

def display_about():
    """Display about information"""
    st.header("ℹ️ About Project Synapse")
    
    st.markdown("""
    ## Overview
    Project Synapse is an autonomous AI coordinator designed to resolve last-mile delivery 
    disruptions using intelligent reasoning and tool execution.
    
    ## Key Features
    - **ReAct Pattern**: Combines reasoning and acting for intelligent decision-making
    - **Tool Integration**: Uses multiple logistics tools for comprehensive problem-solving
    - **Transparent Reasoning**: Provides detailed chain-of-thought for every decision
    - **Real-time Resolution**: Handles disruptions as they occur
    
    ## Available Tools
    - `check_traffic()` - Monitor traffic conditions and incidents
    - `get_merchant_status()` - Check merchant availability and prep times
    - `notify_customer()` - Send customer notifications and updates
    - `reroute_driver()` - Optimize driver routes and assignments
    - `find_nearby_alternatives()` - Locate alternative merchants or services
    - `initiate_refund()` - Process customer refunds and compensations
    - `contact_recipient()` - Communicate with delivery recipients
    - `find_secure_location()` - Locate secure drop-off points
    
    ## Supported Scenarios
    - Restaurant delays and overcrowding
    - Traffic disruptions and route changes
    - Recipient unavailability
    - Merchant issues and disputes
    - Delivery disputes and damage claims
    
    ## Technology Stack
    - **Agent Framework**: LangChain with OpenAI GPT-4 or Google Gemini
    - **Web Interface**: Streamlit
    - **Mock Services**: FastAPI for tool simulation
    - **Logging**: Comprehensive action tracking
    
    ## Recent Fixes
    - ✅ Fixed validation logic for correct solution marking
    - ✅ Improved resolution success determination
    - ✅ Enhanced tool output interpretation
    - ✅ Added comprehensive debugging information
    """)

if __name__ == "__main__":
    main()
