import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.market_agent import fetch_market_data, format_market_cap
from agents.research_agent import run_earnings_agent, run_risk_agent

app = FastAPI(title="Multi-Agent Financial Research Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    ticker: str
    api_key: str = ""


def sse_event(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


async def run_pipeline(ticker: str, api_key: str):
    """Stream the 3-agent pipeline via Server-Sent Events."""

    # ── Agent 1: Market Data ──────────────────────────────────────────────────
    yield sse_event({"agent": "market", "status": "running",
                     "message": f"Fetching live market data for {ticker.upper()}..."})
    await asyncio.sleep(0.3)

    market_data = await asyncio.to_thread(fetch_market_data, ticker)

    if "error" in market_data:
        yield sse_event({"agent": "market", "status": "error",
                         "message": f"Could not fetch data: {market_data['error']}"})
        return

    yield sse_event({
        "agent": "market",
        "status": "done",
        "message": f"Market data retrieved for {market_data['company_name']}",
        "data": {
            "ticker":        market_data["ticker"],
            "company_name":  market_data["company_name"],
            "current_price": market_data["current_price"],
            "change_pct":    market_data["change_pct"],
            "market_cap":    format_market_cap(market_data.get("market_cap", 0)),
            "pe_ratio":      market_data["pe_ratio"],
            "beta":          market_data["beta"],
            "week_52_high":  market_data["week_52_high"],
            "week_52_low":   market_data["week_52_low"],
            "sector":        market_data["sector"],
            "recommendation": market_data["recommendation"],
            "price_history": market_data["price_history"],
        }
    })

    # ── Agent 2: Earnings / Fundamentals ─────────────────────────────────────
    yield sse_event({"agent": "earnings", "status": "running",
                     "message": "Analyzing earnings, fundamentals & valuation..."})
    await asyncio.sleep(0.5)

    earnings = await asyncio.to_thread(run_earnings_agent, market_data, api_key)

    yield sse_event({
        "agent": "earnings",
        "status": "done",
        "message": "Earnings analysis complete",
        "data": earnings
    })

    # ── Agent 3: Risk Analysis ────────────────────────────────────────────────
    yield sse_event({"agent": "risk", "status": "running",
                     "message": "Running risk assessment & building investment thesis..."})
    await asyncio.sleep(0.5)

    risk = await asyncio.to_thread(run_risk_agent, market_data, earnings, api_key)

    yield sse_event({
        "agent": "risk",
        "status": "done",
        "message": "Risk analysis complete",
        "data": risk
    })

    # ── Final signal ──────────────────────────────────────────────────────────
    yield sse_event({"agent": "complete", "status": "done",
                     "message": "Research report ready"})


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    return StreamingResponse(
        run_pipeline(request.ticker.strip().upper(), request.api_key.strip()),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Financial Research Copilot"}


# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
