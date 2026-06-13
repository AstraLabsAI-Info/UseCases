"""Market Intelligence — structured JSON signals from live-web evidence.

Usage:
    export ASTRALABS_API_KEY=sk_live_...
    export OPENAI_API_KEY=sk-...
    python market_intel.py "electric vehicles"
"""
from __future__ import annotations

import json
import os
import sys
import requests
from openai import OpenAI

API_BASE = os.environ.get("ASTRALABS_API_BASE", "https://api.astralabsai.com/v1")
API_KEY = os.environ.get("ASTRALABS_API_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")

llm = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)

PROMPT = (
    "You are a market analyst. Given the topic and the evidence below, "
    "return STRICT JSON with these keys: headline, key_players, "
    "pricing_signals, supply_chain_signals, growth_drivers, risks. "
    "Cite source numbers inline (e.g. [1], [2])."
)


def market_intel(topic: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Set ASTRALABS_API_KEY in your environment.")
    evidence = requests.post(
        f"{API_BASE}/insights",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "query": f"{topic} market intelligence pricing supply chain trends",
            "mode": "quick",
        },
        timeout=60,
    ).json()

    completion = llm.chat.completions.create(
        model=LLM_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": PROMPT},
            {
                "role": "user",
                "content": (
                    f"Topic: {topic}\n\nEvidence:\n"
                    + json.dumps(evidence.get("sources", []))[:8000]
                ),
            },
        ],
    )
    return {
        "topic": topic,
        "signals": json.loads(completion.choices[0].message.content),
        "sources": evidence.get("sources", []),
    }


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) or "electric vehicles"
    print(json.dumps(market_intel(topic), indent=2))
