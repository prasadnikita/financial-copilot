import json

# ─────────────────────────────────────────────
# SMART MOCK FALLBACK (when no API key)
# ─────────────────────────────────────────────

MOCK_EARNINGS = {
    "revenue_analysis": "The company demonstrates solid top-line growth with consistent revenue expansion over the trailing twelve months. Revenue diversification across segments provides resilience against sector-specific headwinds.",
    "valuation": "Current P/E ratio sits at a moderate premium to sector peers, reflecting the market's confidence in future growth. Forward P/E suggests analysts expect continued earnings expansion.",
    "profitability": "Profit margins are healthy compared to industry benchmarks, indicating strong operational efficiency. The company has maintained disciplined cost controls even during inflationary periods.",
    "analyst_sentiment": "Analyst consensus skews positive with price targets suggesting meaningful upside from current levels. Recent rating upgrades reflect improving business fundamentals.",
    "key_strengths": ["Strong brand moat and market position", "Consistent free cash flow generation", "Expanding margin profile"],
    "key_concerns": ["Macroeconomic sensitivity to rate environment", "Competitive pressure in core markets"],
    "earnings_score": 74,
}

MOCK_RISK = {
    "market_risk": "Systematic market risk is moderate given the stock's beta profile relative to broader indices. Sector rotation dynamics and macroeconomic sensitivity present manageable but real headwinds.",
    "volatility_assessment": "Historical volatility patterns suggest the stock tends to amplify market moves, with beta indicating above-average sensitivity to index fluctuations.",
    "downside_scenario": "In a bear case scenario, multiple compression combined with earnings deceleration could drive significant downside from current levels.",
    "upside_scenario": "Bull case hinges on sustained earnings beats and margin expansion driving re-rating. A return to historical peak multiples could yield substantial upside.",
    "risk_factors": ["Interest rate sensitivity on valuation multiples", "Execution risk on growth initiatives", "Competitive disruption from emerging players"],
    "investment_thesis": "This is a quality business trading at a reasonable valuation with a credible path to continued earnings growth. The risk/reward profile is attractive for investors with a 12-18 month time horizon.",
    "risk_rating": "MODERATE",
    "overall_score": 71,
    "action": "BUY",
}


# ─────────────────────────────────────────────
# PUBLIC AGENT FUNCTIONS
# ─────────────────────────────────────────────

def run_earnings_agent(market_data: dict, api_key: str = "") -> dict:
    """
    Run earnings/fundamentals analysis.
    Priority: CrewAI (Claude-powered) → Smart Mock fallback
    """
    if api_key and api_key.strip():
        try:
            from agents.crew_agents import run_fundamentals_crew
            result = run_fundamentals_crew(market_data, api_key)
            if result:
                print("✅ CrewAI Fundamentals Agent succeeded")
                return result
        except Exception as e:
            print(f"CrewAI fallback triggered: {e}")

    # Smart mock — inject real data into template
    mock = MOCK_EARNINGS.copy()
    company  = market_data.get("company_name", market_data.get("ticker", "This company"))
    pe       = market_data.get("pe_ratio", "N/A")
    margin   = market_data.get("profit_margin", "N/A")
    mock["valuation"]     = f"{company} trades at a P/E of {pe}, reflecting market expectations for continued earnings growth. Valuation appears reasonable relative to sector peers given the growth profile."
    mock["profitability"] = f"Profit margins stand at {margin}%, demonstrating the company's ability to convert revenue into bottom-line earnings efficiently."
    score = 70
    if market_data.get("pe_ratio") and market_data["pe_ratio"] < 20: score += 10
    if market_data.get("profit_margin", 0) > 15: score += 5
    mock["earnings_score"] = min(score, 95)
    return mock


def run_risk_agent(market_data: dict, earnings: dict, api_key: str = "") -> dict:
    """
    Run risk analysis.
    Priority: CrewAI (Claude-powered) → Smart Mock fallback
    """
    if api_key and api_key.strip():
        try:
            from agents.crew_agents import run_risk_crew
            result = run_risk_crew(market_data, earnings, api_key)
            if result:
                print("✅ CrewAI Risk Agent succeeded")
                return result
        except Exception as e:
            print(f"CrewAI risk fallback triggered: {e}")

    # Smart mock — inject real data
    mock = MOCK_RISK.copy()
    beta    = market_data.get("beta", 1.0)
    company = market_data.get("company_name", market_data.get("ticker", "The company"))
    mock["volatility_assessment"] = f"{company} has a beta of {beta}, indicating {'above' if beta > 1 else 'below'}-average sensitivity to market movements. This {'amplifies' if beta > 1 else 'dampens'} both upside and downside moves relative to the index."
    mock["risk_rating"] = "HIGH" if beta > 1.5 else "MODERATE" if beta > 0.8 else "LOW"
    score = 75
    if beta < 1: score += 5
    if market_data.get("recommendation") == "BUY": score += 5
    mock["overall_score"] = min(score, 95)
    mock["action"] = market_data.get("recommendation", "HOLD") if market_data.get("recommendation") in ["BUY", "HOLD", "SELL"] else "HOLD"
    return mock
