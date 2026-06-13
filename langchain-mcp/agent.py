"""LangChain tool-calling agent using AstraLabsAI as the live-web tool.

Usage:
    pip install -r requirements.txt
    export ASTRALABS_API_KEY=sk_live_...
    export OPENAI_API_KEY=sk-...
    python agent.py "Who recently raised funding in the AI search space?"
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
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


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
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)
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
