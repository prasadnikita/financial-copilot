# ⚡ FinCopilot — Multi-Agent Financial Research Copilot

A production-grade multi-agent AI system that orchestrates **3 specialized agents** using
**LangGraph**, **Claude AI**, and **real-time market data** to generate automated investment research reports.

---

## 🏗️ Architecture

```
User Input (Ticker)
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│                   LangGraph Orchestrator                 │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────┐  │
│  │ Market Data  │──▶│ Fundamentals │──▶│    Risk    │  │
│  │    Agent     │   │    Agent     │   │   Agent    │  │
│  │  (yfinance)  │   │ (Claude AI)  │   │ (Claude AI)│  │
│  └──────────────┘   └──────────────┘   └────────────┘  │
└─────────────────────────────────────────────────────────┘
       │
       ▼
Investment Research Report (FastAPI + HTML Dashboard)
```

**Tech Stack:** FastAPI · LangGraph · Claude AI · yfinance · SSE Streaming · Chart.js

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
```
http://localhost:8000
```

### 4. (Optional) Add your Claude API key
Enter your Anthropic API key in the UI for AI-powered analysis.
Leave blank to use the intelligent fallback with real market data.

Get a free key at: https://console.anthropic.com

---

## 📁 Project Structure

```
financial-copilot/
├── main.py                    # FastAPI app + SSE streaming endpoint
├── graph.py                   # LangGraph multi-agent orchestration
├── agents/
│   ├── market_agent.py        # Agent 1: Real-time market data (yfinance)
│   └── research_agent.py      # Agent 2 & 3: Earnings + Risk (Claude AI)
├── static/
│   └── index.html             # Full-stack dark financial dashboard
└── requirements.txt
```

---

## 🎯 Demo Script (30-min Interview)

### Opening (2 min)
> "I built a Multi-Agent Financial Research Copilot that mirrors what I
> did at JPMorgan Chase — using LangGraph to orchestrate specialized AI
> agents for automated financial analysis."

### Live Demo (10 min)
1. Open http://localhost:8000
2. Type `NVDA` and click **Analyze**
3. Point out the 3 agents activating in sequence
4. Show real-time price chart populating
5. Walk through the AI-generated investment thesis
6. Try `TSLA` — show how risk rating changes

### Architecture Walkthrough (5 min)
```python
# In graph.py — show LangGraph state machine
graph.add_node("market_data", market_data_node)
graph.add_node("earnings",    earnings_node)
graph.add_node("risk",        risk_node)
graph.set_entry_point("market_data")
```
> "Each agent receives the output of the previous one as context —
> exactly how I designed the fraud investigation pipeline at JPMC."

### Key Talking Points
- **SSE Streaming**: Real-time agent status updates (like Kafka consumers)
- **Smart Fallback**: Works without API key — important for production resilience
- **Claude tool-calling**: Same pattern I used for fraud investigation agents
- **LangGraph orchestration**: State machine with conditional edges for error handling

---

## 💡 Key Features

| Feature | Implementation |
|---------|---------------|
| Real-time stock data | yfinance (no API key needed) |
| Multi-agent orchestration | LangGraph StateGraph |
| AI analysis | Anthropic Claude (claude-sonnet-4) |
| Streaming updates | Server-Sent Events (SSE) |
| Resilient fallback | Smart mock with real data injection |
| Production patterns | FastAPI + Docker-ready |

---

## 🔧 Extending This Project (Interview Bonus Points)

- **Add Kafka**: Stream live price alerts (mention JPMC experience)
- **Add Pinecone**: RAG over earnings call transcripts
- **Add Twilio**: SMS alerts when risk rating changes
- **Add CrewAI**: Multi-agent debate between bull/bear analysts
- **Add Airtable**: CRM logging for tracked stocks
