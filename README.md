# Project Synapse - Complete Setup Guide

## System Requirements & Prerequisites

**Operating System:** Windows, macOS, or Linux  
**RAM:** 4GB minimum (8GB recommended)  
**Storage:** 500MB free space  
**Internet:** Required for AI API calls  

## Complete Step-by-Step Setup (From t=0)

### Step 1: Install Python (if not already installed)

**For Windows:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.9 or newer (3.11 recommended)
3. Run the installer and **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

```

**Verify Installation:**
Open terminal/command prompt and type:
```bash
python --version
# Should show Python 3.9+ 

pip --version
# Should show pip version
```

### Step 2: Get Your Free Google Gemini API Key

1. Go to https://aistudio.google.com/
2. Sign in with any Google account (Gmail works)
3. Click "Get API Key" in the top menu
4. Click "Create API key"
5. Copy the key that appears - save it somewhere safe!

### Step 3: Download and Extract Project

1. Download `project-synapse.zip` 
2. Extract to a folder on your PC (e.g., `C:\Users\YourName\project-synapse` or `/home/yourname/project-synapse`)
3. Open terminal/command prompt
4. Navigate to the extracted folder:
   ```bash
   cd path/to/project-synapse
   ```

### Step 4: Set Up API Key Environment Variable

**For Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-actual-key-here
```

**For Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-actual-key-here"
```

**For macOS/Linux:**
```bash
export GEMINI_API_KEY="your-actual-key-here"
```

**Alternative (Works on all systems) - Create .env file:**
1. Create a new file called `.env` in the project folder
2. Add this line: `GEMINI_API_KEY=your-actual-key-here`
3. Install python-dotenv: `pip install python-dotenv`

### Step 5: Install Required Python Packages

Run this command in your project folder:
```bash
pip install streamlit langchain langchain-google-genai langchain-core pandas plotly fastapi uvicorn pydantic requests google-genai
```

**If you get permission errors on Windows, try:**
```bash
pip install --user streamlit langchain langchain-google-genai langchain-core pandas plotly fastapi uvicorn pydantic requests google-genai
```

### Step 6: Run the Application

In your project folder, run:
```bash
streamlit run app.py --server.port 5000
```

**Expected Output:**
```
Collecting usage statistics...
You can now view your Streamlit app in your browser.
Local URL: http://localhost:5000
```

### Step 7: Access the Application

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the Project Synapse interface!

## What You'll See & How to Test

1. **Homepage:** Shows "Project Synapse - Agentic Last-Mile Coordinator"
2. **API Status:** Green checkmark showing "Gemini API Key configured"
3. **Sample Scenarios:** Choose from pre-built delivery disruption scenarios
4. **Test the System:** 
   - Select "Restaurant Overload - GrabFood" scenario
   - Click "Execute Resolution" 
   - Watch the AI analyze and solve the problem step-by-step!

## Troubleshooting Common Issues

**Problem:** "streamlit command not found"  
**Solution:** Try `python -m streamlit run app.py --server.port 5000`

**Problem:** "Module not found" errors  
**Solution:** Make sure you're in the correct folder and all packages installed successfully

**Problem:** API key errors  
**Solution:** Double-check your GEMINI_API_KEY is set correctly

**Problem:** Port 5000 already in use  
**Solution:** Change port: `streamlit run app.py --server.port 8080`

## Success Verification

You'll know everything works when:
- ✅ Web interface loads without errors
- ✅ Green checkmark for API key status
- ✅ Can select and run a sample scenario
- ✅ See step-by-step AI reasoning and tool usage
- ✅ Dashboard shows metrics and performance data

## Project Structure

The downloaded zip contains:

```
project-synapse/
├── app.py                    # Main Streamlit web application
├── README.md                 # Complete setup and usage guide  
├── pyproject.toml           # Python dependencies configuration
├── agent/
│   ├── synapse_agent.py     # Core AI agent with ReAct pattern
│   ├── tools.py             # 10+ logistics tools collection
│   └── prompts.py           # AI system prompts and templates
├── services/
│   └── mock_apis.py         # Realistic logistics API simulations
├── scenarios/
│   └── test_scenarios.py    # Real-world delivery disruption scenarios
├── utils/
│   └── logger.py            # Comprehensive logging system
└── .streamlit/
    └── config.toml          # Web server configuration
```

## About Project Synapse

Project Synapse implements an AI-powered solution that moves beyond traditional rule-based systems by providing autonomous resolution of complex delivery scenarios. Using the ReAct pattern (Reasoning + Acting), the system can analyze disruptions, use various logistics tools, and execute multi-step resolution plans.

## ✨ Key Features

- **Autonomous Decision Making**: Uses GPT-5 with ReAct pattern for intelligent reasoning
- **Comprehensive Tool Suite**: 10+ logistics tools for traffic, merchants, communications, and more  
- **Transparent Reasoning**: Full chain-of-thought logging for every decision
- **Real-time Resolution**: Handles disruptions as they occur with <30s response times
- **Multi-service Support**: Works across GrabFood, GrabCar, GrabExpress, and GrabMart
- **Performance Tracking**: Built-in metrics dashboard and execution history

The system is completely self-contained with realistic mock services, allowing you to test all delivery coordination features without needing actual logistics APIs.

---

*For support or questions, refer to the README.md file included in the project.*
