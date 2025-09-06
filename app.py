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

os.environ["OPENAI_API_KEY"] = "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"


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
    
    # Display API key status
    openai_key = os.getenv("OPENAI_API_KEY", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    
    if openai_key:
        st.success("✅ OpenAI API Key configured (GPT-5)")
    elif gemini_key:
        st.success("✅ Gemini API Key configured (Gemini-2.5-Flash)")
        st.info("ℹ️ Using Google Gemini as the AI provider")
    else:
        st.error("❌ No AI API Key found. Please set either OPENAI_API_KEY or GEMINI_API_KEY environment variable.")
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
            list(metrics['tools_used'].items()),
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
    """Update performance metrics"""
    metrics = st.session_state.performance_metrics
    
    metrics['total_scenarios'] += 1
    if result.get('resolution_success', False):
        metrics['successful_resolutions'] += 1
    
    # Update average response time
    total_time = metrics['average_response_time'] * (metrics['total_scenarios'] - 1) + execution_time
    metrics['average_response_time'] = total_time / metrics['total_scenarios']
    
    # Update tools usage
    for step in result.get('reasoning_steps', []):
        tool_name = step.get('tool_used')
        if tool_name:
            metrics['tools_used'][tool_name] = metrics['tools_used'].get(tool_name, 0) + 1

def display_execution_results(result, execution_time):
    """Display the execution results with chain of thought"""
    st.success(f"✅ Execution completed in {execution_time:.2f} seconds")
    
    # Final resolution
    st.subheader("🎯 Final Resolution")
    resolution_status = "✅ Successful" if result.get('resolution_success', False) else "❌ Failed"
    st.markdown(f"**Status:** {resolution_status}")
    st.markdown(f"**Solution:** {result.get('final_solution', 'No solution provided')}")
    
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
    else:
        st.info("No reasoning steps recorded.")
    
    # Action trace
    st.subheader("📝 Action Trace")
    action_trace = result.get('action_trace', [])
    if action_trace:
        trace_df = pd.DataFrame(action_trace)
        st.dataframe(trace_df, use_container_width=True)
    
    # Save to history
    st.session_state.execution_history.append({
        'timestamp': datetime.now(),
        'scenario': st.session_state.get('current_scenario', ''),
        'result': result,
        'execution_time': execution_time
    })

def display_history():
    """Display execution history"""
    st.header("📜 Execution History")
    
    if st.session_state.execution_history:
        for i, execution in enumerate(reversed(st.session_state.execution_history)):
            with st.expander(f"Execution {len(st.session_state.execution_history) - i} - {execution['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                st.markdown(f"**Scenario:** {execution['scenario'][:200]}...")
                st.markdown(f"**Success:** {'✅' if execution['result'].get('resolution_success') else '❌'}")
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
    
    

if __name__ == "__main__":
    main()
