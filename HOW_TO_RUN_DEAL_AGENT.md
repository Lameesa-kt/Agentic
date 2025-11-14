# How to Run Deal Agent System

Simple step-by-step guide to run all 5 services needed for the Deal Agent system.

---

## Prerequisites

Before starting, make sure you have:
- **Python 3.10+** installed
- **Node.js** installed
- **Google API Key** (Gemini) - you'll need this for terminals 2, 4, and 5

---

## Quick Start: Run All 5 Terminals

Open **5 separate PowerShell terminals** and run the commands below in order.

---

### **Terminal 1: Toolbox MCP Server** (Port 5000)

**What it does:** Provides database access for Sales Agent

**Commands:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1\sales_agent\database"
$env:SQLITE_DATABASE = ".\customer.sqlite"
.\toolbox.exe --prebuilt sqlite --port 5000
```

**What you'll see:**
```
Starting Toolbox MCP server on port 5000...
Server running...
```

**✅ Keep this terminal open!**

---

### **Terminal 2: Sales Agent** (Port 8000)

**What it does:** Looks up customer information

**Commands:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1\sales_agent"
$env:GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
python fastapi_server.py
```

**Replace `YOUR_GEMINI_API_KEY` with your actual Google API key.**

**What you'll see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Keep this terminal open!**

---

### **Terminal 3: Deal Server** (Port 3000)

**What it does:** Serves deal data from JSON files

**Commands:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1\DealAgent"
npm install
node server.js
```

**Note:** `npm install` is only needed the first time.

**What you'll see:**
```
Mock API running on port 3000
```

**✅ Keep this terminal open!**

---

### **Terminal 4: DealAgent API** (Port 8001)

**What it does:** Main API that combines Sales Agent and Deal Server

**Commands:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1"
$env:GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
python DealAgent\fastapi_server.py
```

**Replace `YOUR_GEMINI_API_KEY` with your actual Google API key.**

**What you'll see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
DealAgent FastAPI is running
```

**✅ Keep this terminal open!**

---

### **Terminal 5: Orchestrator Agent** (Interactive)

**What it does:** Interactive agent where you type your questions

**Commands:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1"
$env:GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
adk run OrchAgent
```

**Replace `YOUR_GEMINI_API_KEY` with your actual Google API key.**

**What you'll see:**
```
Starting OrchAgent...
Agent ready. Type your queries below.
[user]: 
```

**✅ This is where you type your questions!**

---

## How to Run JSON Agent

The JSON Agent is used for modifying JSON data. It runs separately from the main Deal Agent system.

### **JSON Agent** (Port 8002)

**What it does:** Modifies JSON data based on natural language prompts

**Commands:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1\JSON_AGENT-main"
python web/app.py
```

**What you'll see:**
```
Starting JSON Agent FastAPI server on http://0.0.0.0:8002
Web UI: http://localhost:8002/
API Docs: http://localhost:8002/docs
```

**Access the JSON Agent:**
- **Web UI:** http://localhost:8002/
- **API Docs:** http://localhost:8002/docs

**✅ Keep this terminal open if you need JSON modification features!**

---

## Testing

Once all 5 terminals are running, go to **Terminal 5** and type:

```
Find CompanyABC's deal
```

**Expected response:**
```
[user]: Find CompanyABC's deal
[Deal_agent]: ```json
{"status": "success", "customer_id": 1, "company_name": "CompanyABC", "deal": {"bidStart": {"bidAcct": [{"abrEnab": null, "abrEnabUpd": null, "acet": "00008905R1", "ccElig": null, "ccEligUpd": null, "cwtTierClsUpd": null, "cwtTiercls": null, "payTerm": "30", "payTermCode": "03", "payTermCodeUpd": null, "payTermUpd": null}, {"abrEnab": "Y", "abrEnabUpd": null, "acet": "0000G8R287", "ccElig": "yes", "ccEligUpd": null, "cwtTierClsUpd": null, "cwtTiercls": null, "payTerm": "20", "payTermCode": "03", "payTermCodeUpd": null, "payTermUpd": null}], "bidHead": {"bidName": "By Crea AB", "bidNum": "D001149727", "billToCny": "SE", "cny": "SE", "creBxId": "XLQOBBL", "creDte": "2025-09-17", "dealRsn": "Conversion", "dealStatus": "P", "dist": "12", "endDte": "2099-01-03", "estAnnGrs": 2904828, "lastModDte": "2025-09-26", "origBid": "0001133442", "owner": "Marcus Persson", "rateTypCd": "01-1", "reg": "16", "sttDte": "2025-09-27", "templateMaster": "D001003339", "templateName": "SE Ronja V.3 [Non-Static]", "ver": null}}}}
```
[user]: 
```

---

## Verification Checklist

Before testing, make sure all terminals show:

- [ ] **Terminal 1:** "Server running on port 5000"
- [ ] **Terminal 2:** "Uvicorn running on http://0.0.0.0:8000"
- [ ] **Terminal 3:** "Mock API running on port 3000"
- [ ] **Terminal 4:** "Uvicorn running on http://0.0.0.0:8001"
- [ ] **Terminal 5:** "[user]:" prompt

You can also check in your browser:
- Sales Agent: http://localhost:8000/
- Deal Server: http://localhost:3000/api/getdeal/customer/1
- DealAgent: http://localhost:8001/
- JSON Agent: http://localhost:8002/

---

## Troubleshooting

### Port Already in Use

If you see "port already in use":

```powershell
# Find what's using the port (replace 8000 with your port number)
netstat -aon | findstr :8000

# Kill the process (replace <PID> with the number from above)
taskkill /PID <PID> /F
```

### Toolbox Not Found

If `toolbox.exe` is missing:

```powershell
cd "D:\ded\FinalDeal - Copy git 1\sales_agent\database"
Invoke-WebRequest -Uri "https://storage.googleapis.com/genai-toolbox/v0.18.0/windows/amd64/toolbox.exe" -OutFile "toolbox.exe"
```

### Missing Dependencies

```powershell
# Install Python packages
pip install fastapi uvicorn httpx google-adk toolbox-llamaindex

# Install Node.js packages
cd "D:\ded\FinalDeal - Copy git 1\DealAgent"
npm install
```

### ADK Command Not Found

If `adk` command doesn't work:

```powershell
pip install google-adk
python -m google.adk.cli run OrchAgent
```

---

## System Overview

```
Orchestrator Agent (Terminal 5)
    ↓
DealAgent API (Terminal 4) → Port 8001
    ├─→ Sales Agent (Terminal 2) → Port 8000 → Toolbox (Terminal 1) → Port 5000
    └─→ Deal Server (Terminal 3) → Port 3000
```

**Flow:**
1. You type a question in Terminal 5 (Orchestrator)
2. Orchestrator sends it to DealAgent API (Terminal 4)
3. DealAgent queries Sales Agent (Terminal 2) to find customer ID
4. Sales Agent uses Toolbox (Terminal 1) to access database
5. DealAgent gets deal data from Deal Server (Terminal 3)
6. DealAgent returns complete JSON response

---

## All Commands Reference

Copy-paste ready commands for all 5 terminals:

**Terminal 1:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1\sales_agent\database"
$env:SQLITE_DATABASE = ".\customer.sqlite"
.\toolbox.exe --prebuilt sqlite --port 5000
```

**Terminal 2:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1\sales_agent"
$env:GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
python fastapi_server.py
```

**Terminal 3:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1\DealAgent"
node server.js
```

**Terminal 4:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1"
$env:GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
python DealAgent\fastapi_server.py
```

**Terminal 5:**
```powershell
cd "D:\ded\FinalDeal - Copy git 1"
$env:GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
adk run OrchAgent
```

**JSON Agent (Optional - for JSON modification):**
```powershell
cd "D:\ded\FinalDeal - Copy git 1\JSON_AGENT-main"
python web/app.py
```

---

**That's it!** Follow the steps above and you'll have the system running.
