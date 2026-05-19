# ⚡ FinCopilot — Multi-Agent Financial Research Copilot

A production-grade multi-agent AI system that orchestrates **3 specialized agents** using
**LangGraph**, **CrewAI**, **Claude AI**, and real-time market data to generate automated investment research reports.

---

## 🏗️ Architecture
User Input (Ticker)
│
▼
┌─────────────────────────────────────────────────────────┐
│                   LangGraph Orchestrator                 │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────┐  │
│  │ Market Data  │──▶│ Fundamentals │──▶│    Risk    │  │
│  │    Agent     │   │    Agent     │   │   Agent    │  │
│  │ (Yahoo API)  │   │   (CrewAI    │   │  (CrewAI   │  │
│  │              │   │  + Claude)   │   │ + Claude)  │  │
│  └──────────────┘   └──────────────┘   └────────────┘  │
└─────────────────────────────────────────────────────────┘
│
▼
Investment Research Report (FastAPI + HTML Dashboard)

**Tech Stack:** FastAPI · LangGraph · CrewAI · Claude AI · SSE Streaming · Chart.js

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Open the dashboard
http://localhost:8000

### 4. (Optional) Add your Claude API key
Enter your Anthropic API key in the UI for AI-powered analysis.
Leave blank to use the intelligent fallback with real market data.

Get a free key at: https://console.anthropic.com

---

## 📁 Project Structure
financial-copilot/
├── main.py                    # FastAPI app + SSE streaming endpoint
├── graph.py                   # LangGraph multi-agent orchestration
├── agents/
│   ├── market_agent.py        # Agent 1: Real-time market data (Yahoo Finance API)
│   ├── crew_agents.py         # CrewAI agent definitions with roles & backstories
│   └── research_agent.py      # Agent 2 & 3: Earnings + Risk (CrewAI + Claude AI)
├── static/
│   └── index.html             # Full-stack dark financial dashboard
└── requirements.txt

---

## 🤖 How LangGraph + CrewAI Work Together
LangGraph (Orchestrator)        CrewAI (Agent Roles)
────────────────────────        ────────────────────
graph.py manages the            crew_agents.py defines:
pipeline state & flow
Agent 2:
Node 1 → market_agent    →      Role: "Senior Fundamentals Analyst"
Node 2 → earnings_node   →      Backstory: "CFA, 15yrs Goldman Sachs"
Node 3 → risk_node       →      Role: "Quantitative Risk Analyst"
Backstory: "PhD MIT, ex-hedge fund"
↓
Claude AI powers each agent

- **LangGraph** manages the overall pipeline, state, and flow control
- **CrewAI** defines each agent's role, goal, and professional backstory
- **Claude AI** is the LLM brain powering every CrewAI agent

---

## 🎯 Demo Script (30-min Interview)

### Opening (2 min)
> "I built a Multi-Agent Financial Research Copilot using LangGraph to orchestrate
> specialized CrewAI agents — the same architecture I used at JPMorgan Chase for
> automated fraud investigation workflows."

### Live Demo (10 min)
1. Open `http://localhost:8000`
2. Type `NVDA` and click **Analyze**
3. Point out the 3 agents activating in sequence
4. Show real-time price chart populating
5. Walk through the AI-generated investment thesis
6. Try `TSLA` — show how risk rating changes

### Architecture Walkthrough (5 min)
```python
# graph.py — LangGraph state machine
graph.add_node("market_data", market_data_node)
graph.add_node("earnings",    earnings_node)
graph.add_node("risk",        risk_node)
graph.set_entry_point("market_data")

# crew_agents.py — CrewAI agent with role
fundamentals_analyst = Agent(
    role="Senior Financial Fundamentals Analyst",
    goal="Analyze earnings quality and valuation metrics",
    backstory="CFA charterholder, 15 years at Goldman Sachs...",
    llm=claude,
)
```

### Key Talking Points
- **SSE Streaming**: Real-time agent status updates (like Kafka consumers)
- **LangGraph + CrewAI**: Same orchestration pattern as JPMC fraud pipeline
- **Smart Fallback**: Works without API key — production resilience
- **Claude AI**: Same LLM stack used at JPMorgan Chase

---

## 💡 Key Features

| Feature | Implementation |
|---------|---------------|
| Real-time stock data | Yahoo Finance API (direct, no key needed) |
| Multi-agent orchestration | LangGraph StateGraph |
| Agent roles & personas | CrewAI Agents with backstories |
| AI analysis | Anthropic Claude (claude-sonnet-4) |
| Streaming updates | Server-Sent Events (SSE) |
| Resilient fallback | Smart mock with real data injection |
| Production patterns | FastAPI + Docker-ready |

---

## 🔧 Extending This Project

- **Add Pinecone**: RAG over earnings call transcripts
- **Add Kafka**: Stream live price alerts
- **Add Twilio**: SMS alerts when risk rating changes
- **Add Airtable**: CRM logging for tracked stocks