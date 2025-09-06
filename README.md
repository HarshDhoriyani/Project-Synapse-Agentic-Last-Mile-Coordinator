# Project Synapse - Agentic Last-Mile Coordinator

An autonomous AI coordinator that resolves last-mile delivery disruptions using intelligent reasoning and tool execution.

## 🎯 Overview

Project Synapse implements an AI-powered solution that moves beyond traditional rule-based systems by providing autonomous resolution of complex delivery scenarios. Using the ReAct pattern (Reasoning + Acting), the system can analyze disruptions, use various logistics tools, and execute multi-step resolution plans.

## ✨ Key Features

- **Autonomous Decision Making**: Uses GPT-5 with ReAct pattern for intelligent reasoning
- **Comprehensive Tool Suite**: 10+ logistics tools for traffic, merchants, communications, and more  
- **Transparent Reasoning**: Full chain-of-thought logging for every decision
- **Real-time Resolution**: Handles disruptions as they occur with <30s response times
- **Multi-service Support**: Works across GrabFood, GrabCar, GrabExpress, and GrabMart
- **Performance Tracking**: Built-in metrics dashboard and execution history

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher  
- Either OpenAI API key OR Google Gemini API key (Gemini has free tier!)

### Installation

1. **Clone or download the project files**

2. **Set up environment variable (choose one)**
   
   **Option A: Using Google Gemini (Free!):**
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key-here"
   ```
   Get your free key at: https://aistudio.google.com/
   
   **Option B: Using OpenAI GPT-5:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit langchain langchain-openai langchain-core fastapi uvicorn pydantic requests pandas plotly
   ```

4. **Run the application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

5. **Access the web interface**
   - Open your browser to `http://localhost:5000`
   - The application will be ready to use!

## 🛠️ Architecture

