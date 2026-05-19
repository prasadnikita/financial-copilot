from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.market_agent import fetch_market_data
from agents.research_agent import run_earnings_agent, run_risk_agent


# ─── State ────────────────────────────────────────────────────────────────────

class ResearchState(TypedDict):
    ticker: str
    api_key: str
    market_data: Optional[dict]
    earnings_analysis: Optional[dict]
    risk_analysis: Optional[dict]
    error: Optional[str]


# ─── Node Functions ────────────────────────────────────────────────────────────

def market_data_node(state: ResearchState) -> ResearchState:
    """Agent 1: Fetch real-time market data."""
    data = fetch_market_data(state["ticker"])
    if "error" in data:
        return {**state, "error": data["error"]}
    return {**state, "market_data": data}


def earnings_node(state: ResearchState) -> ResearchState:
    """Agent 2: Analyze earnings and fundamentals."""
    if state.get("error") or not state.get("market_data"):
        return state
    analysis = run_earnings_agent(state["market_data"], state.get("api_key", ""))
    return {**state, "earnings_analysis": analysis}


def risk_node(state: ResearchState) -> ResearchState:
    """Agent 3: Assess risk and generate investment thesis."""
    if state.get("error") or not state.get("earnings_analysis"):
        return state
    risk = run_risk_agent(
        state["market_data"],
        state["earnings_analysis"],
        state.get("api_key", "")
    )
    return {**state, "risk_analysis": risk}


def should_continue(state: ResearchState) -> str:
    return "end" if state.get("error") else "continue"


# ─── Build Graph ───────────────────────────────────────────────────────────────

def build_research_graph() -> StateGraph:
    graph = StateGraph(ResearchState)

    graph.add_node("market_data", market_data_node)
    graph.add_node("earnings",    earnings_node)
    graph.add_node("risk",        risk_node)

    graph.set_entry_point("market_data")

    graph.add_conditional_edges(
        "market_data",
        should_continue,
        {"continue": "earnings", "end": END}
    )
    graph.add_conditional_edges(
        "earnings",
        should_continue,
        {"continue": "risk", "end": END}
    )
    graph.add_edge("risk", END)

    return graph.compile()


# Singleton compiled graph
research_graph = build_research_graph()
