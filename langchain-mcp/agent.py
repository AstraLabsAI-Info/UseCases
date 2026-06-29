"""LangChain tool-calling agent using AstraLabsAI as the live-web tool.

Usage:
    pip install -r requirements.txt
    cp .env.example .env   # then fill in LLM_API_KEY / LLM_BASE_URL / LLM_MODEL
    export $(grep -v '^#' .env | xargs)
    python agent.py "Who recently raised funding in the AI search space?"

Works with any OpenAI-compatible provider (OpenAI, xAI Grok, Google Gemini,
DeepSeek, Qwen, Moonshot/Kimi, ...). See .env.example for current base URLs —
always confirm the latest URL on the provider's own docs.
"""
from __future__ import annotations

import os
import sys
import requests

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate

API_BASE = os.environ.get("ASTRALABS_API_BASE", "https://api.astralabsai.com/v1")
ASTRALABS_API_KEY = os.environ["ASTRALABS_API_KEY"]
# Generic OpenAI-compatible LLM config (fallback to OPENAI_* for back-compat)
LLM_API_KEY = os.environ.get("LLM_API_KEY") or os.environ["OPENAI_API_KEY"]
LLM_BASE_URL = os.environ.get("LLM_BASE_URL") or os.environ.get(
    "OPENAI_BASE_URL", "https://api.openai.com/v1"
)
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")


@tool
def astralabs_search(query: str) -> dict:
    """Search the live web with AstraLabsAI. Returns summarized results with sources."""
    r = requests.post(
        f"{API_BASE}/insights",
        headers={"Authorization": f"Bearer {ASTRALABS_API_KEY}"},
        json={"query": query, "mode": "quick"},
        timeout=30,
    )
    return r.json()


def build_executor() -> AgentExecutor:
    llm = ChatOpenAI(
        model=LLM_MODEL, temperature=0, api_key=LLM_API_KEY, base_url=LLM_BASE_URL
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a research agent. Always use astralabs_search before answering."),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_openai_tools_agent(llm, [astralabs_search], prompt)
    return AgentExecutor(agent=agent, tools=[astralabs_search], verbose=True)


def main() -> None:
    question = " ".join(sys.argv[1:]) or "Who recently raised funding in the AI search space?"
    executor = build_executor()
    result = executor.invoke({"input": question})
    print("\n=== Final answer ===\n")
    print(result.get("output", result))


if __name__ == "__main__":
    main()
