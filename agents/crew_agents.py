import json
import os
from crewai import Agent, Task, Crew, Process
from langchain_anthropic import ChatAnthropic


def _get_llm(api_key: str):
    """Create Claude LLM for CrewAI agents."""
    os.environ["ANTHROPIC_API_KEY"] = api_key
    return ChatAnthropic(
        model="claude-sonnet-4-20250514",
        anthropic_api_key=api_key,
        max_tokens=1000,
    )


# ─────────────────────────────────────────────────────────────────
# AGENT 2: FUNDAMENTALS ANALYST (CrewAI)
# ─────────────────────────────────────────────────────────────────

def run_fundamentals_crew(market_data: dict, api_key: str) -> dict | None:
    """
    Uses a CrewAI Fundamentals Analyst agent to analyze earnings & valuation.
    Returns structured JSON dict or None if it fails.
    """
    try:
        llm = _get_llm(api_key)

        # Define the CrewAI Agent with a role, goal, and backstory
        fundamentals_analyst = Agent(
            role="Senior Financial Fundamentals Analyst",
            goal=(
                "Analyze a company's earnings quality, valuation metrics, "
                "and profitability to produce a structured investment-grade report."
            ),
            backstory=(
                "You are a CFA charterholder with 15 years on Wall Street analyzing "
                "company fundamentals. You've worked at Goldman Sachs and Fidelity, "
                "and you are known for catching hidden risks in P/E ratios and margins "
                "that others miss. You always respond in clean JSON format."
            ),
            llm=llm,
            verbose=False,
            allow_delegation=False,
        )

        # Define the Task this agent must complete
        task = Task(
            description=(
                f"Analyze the following stock data and produce a fundamentals report.\n\n"
                f"Stock Data:\n{json.dumps(market_data, indent=2)}\n\n"
                f"Return ONLY valid JSON with these exact keys:\n"
                f"revenue_analysis, valuation, profitability, analyst_sentiment, "
                f"key_strengths (list of 3), key_concerns (list of 2), earnings_score (0-100 int)."
            ),
            expected_output=(
                "A valid JSON object with keys: revenue_analysis, valuation, "
                "profitability, analyst_sentiment, key_strengths, key_concerns, earnings_score."
            ),
            agent=fundamentals_analyst,
        )

        # Create and run the Crew
        crew = Crew(
            agents=[fundamentals_analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff()
        raw = str(result).strip()

        # Strip markdown fences if present
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw.strip())

    except Exception as e:
        print(f"CrewAI fundamentals agent error: {e}")
        return None


# ─────────────────────────────────────────────────────────────────
# AGENT 3: RISK ANALYST (CrewAI)
# ─────────────────────────────────────────────────────────────────

def run_risk_crew(market_data: dict, earnings: dict, api_key: str) -> dict | None:
    """
    Uses a CrewAI Risk Analyst agent to assess risk and generate investment thesis.
    Returns structured JSON dict or None if it fails.
    """
    try:
        llm = _get_llm(api_key)

        # Define the CrewAI Agent
        risk_analyst = Agent(
            role="Quantitative Risk Analyst",
            goal=(
                "Assess investment risk, identify upside/downside scenarios, "
                "and generate a clear BUY/HOLD/SELL recommendation with thesis."
            ),
            backstory=(
                "You are a former hedge fund risk manager with a PhD in Financial "
                "Engineering from MIT. You ran the risk desk at a $10B quant fund "
                "and are known for your razor-sharp risk/reward analysis. "
                "You always respond in clean JSON format."
            ),
            llm=llm,
            verbose=False,
            allow_delegation=False,
        )

        # Define the Task
        task = Task(
            description=(
                f"Assess the investment risk for this stock and generate a thesis.\n\n"
                f"Market Data:\n{json.dumps(market_data, indent=2)}\n\n"
                f"Earnings Analysis:\n{json.dumps(earnings, indent=2)}\n\n"
                f"Return ONLY valid JSON with these exact keys:\n"
                f"market_risk, volatility_assessment, downside_scenario, upside_scenario, "
                f"risk_factors (list of 3), investment_thesis, "
                f"risk_rating (LOW|MODERATE|HIGH), overall_score (0-100 int), "
                f"action (BUY|HOLD|SELL|WATCH)."
            ),
            expected_output=(
                "A valid JSON object with keys: market_risk, volatility_assessment, "
                "downside_scenario, upside_scenario, risk_factors, investment_thesis, "
                "risk_rating, overall_score, action."
            ),
            agent=risk_analyst,
        )

        # Create and run the Crew
        crew = Crew(
            agents=[risk_analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff()
        raw = str(result).strip()

        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw.strip())

    except Exception as e:
        print(f"CrewAI risk agent error: {e}")
        return None
