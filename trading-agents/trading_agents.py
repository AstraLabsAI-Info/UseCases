"""Trading Agents Demo — multi-agent equity research over any world market.

EDUCATIONAL DEMO ONLY. NOT FINANCIAL ADVICE.

Usage:
    pip install -r requirements.txt
    cp .env.example .env   # fill in LLM_API_KEY / LLM_BASE_URL / LLM_MODEL
    export $(grep -v '^#' .env | xargs)
    python trading_agents.py "Top semiconductor stock in Japan"

Works with any OpenAI-compatible LLM (OpenAI, xAI Grok, Google Gemini,
DeepSeek, Qwen, Moonshot/Kimi). Verify base URLs on the provider's docs.
"""
from __future__ import annotations

import json
import os
import sys
import requests
from openai import OpenAI

API_BASE = os.environ.get("ASTRALABS_API_BASE", "https://api.astralabsai.com/v1")
ASTRALABS_API_KEY = os.environ["ASTRALABS_API_KEY"]
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")

client = OpenAI(
    api_key=os.environ.get("LLM_API_KEY") or os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("LLM_BASE_URL")
    or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)


def astralabs_search(query: str) -> dict:
    r = requests.post(
        f"{API_BASE}/insights",
        headers={"Authorization": f"Bearer {ASTRALABS_API_KEY}"},
        json={"query": query, "mode": "quick"},
        timeout=30,
    )
    return r.json()


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "astralabs_search",
            "description": "Search live web for news, filings, prices, sentiment.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    }
]


def _run_tool_calls(msg) -> list:
    """Execute every tool_call on a message and return matching tool messages."""
    out = []
    for call in msg.tool_calls or []:
        args = json.loads(call.function.arguments or "{}")
        result = astralabs_search(args.get("query", ""))
        out.append(
            {
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result)[:5000],
            }
        )
    return out


def resolve_ticker(query: str) -> dict:
    """Turn a natural-language request into a concrete exchange-qualified ticker."""
    msgs = [
        {
            "role": "system",
            "content": (
                "Map the user's investing question to ONE publicly listed equity on any "
                "world market. You may call astralabs_search once."
            ),
        },
        {"role": "user", "content": f'Request: "{query}"'},
    ]
    r = client.chat.completions.create(
        model=LLM_MODEL, messages=msgs, tools=TOOLS, temperature=0.2
    )
    msg = r.choices[0].message
    if msg.tool_calls:
        msgs.append(msg)
        msgs.extend(_run_tool_calls(msg))
    msgs.append(
        {
            "role": "user",
            "content": (
                'Reply ONLY with JSON: {"ticker":"NVDA|7203.T|0700.HK|BMW.DE|RELIANCE.NS",'
                '"exchange":"...","market":"...","company":"...","currency":"..."}'
            ),
        }
    )
    out = client.chat.completions.create(
        model=LLM_MODEL,
        messages=msgs,
        temperature=0,
        response_format={"type": "json_object"},
    ).choices[0].message.content
    return json.loads(out)


AGENTS = [
    ("Market Analyst", "Recent price action, momentum, technicals.", True),
    ("News & Sentiment Analyst", "Recent news, filings, social sentiment.", True),
    ("Bull Researcher", "Strongest bull case.", False),
    ("Bear Researcher", "Strongest bear case.", False),
    ("Risk Manager", "Downside risks, sizing, stops.", False),
]


def run_agent(name: str, role: str, use_tool: bool, ticker: str, market: str, context: str) -> str:
    msgs = [
        {
            "role": "system",
            "content": f"You are the {name} analyzing {ticker} ({market}). {role}",
        },
        {
            "role": "user",
            "content": f"Ticker: {ticker}\nMarket: {market}\n\nTeam context:\n{context}",
        },
    ]
    kwargs = {"model": LLM_MODEL, "messages": msgs, "temperature": 0.3}
    if use_tool:
        kwargs["tools"] = TOOLS
    msg = client.chat.completions.create(**kwargs).choices[0].message
    if use_tool and msg.tool_calls:
        msgs.append(msg)
        msgs.extend(_run_tool_calls(msg))
        msg = client.chat.completions.create(
            model=LLM_MODEL, messages=msgs, temperature=0.4
        ).choices[0].message
    return msg.content or ""


def trade(query: str) -> None:
    r = resolve_ticker(query)
    ticker = r["ticker"]
    market = f"{r.get('market', '')} · {r.get('exchange', '')}"
    print(f"\nResolved → {ticker} ({r.get('company', '')}, {market})\n")
    context = ""
    for name, role, tool in AGENTS:
        out = run_agent(name, role, tool, ticker, market, context)
        print(f"\n### {name}\n{out}\n")
        context += f"\n\n## {name}\n{out}"
    decision = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Head Trader. Reply ONLY with JSON: "
                    "{action, confidence, horizon, thesis, key_risks, catalysts}"
                ),
            },
            {"role": "user", "content": f"Team analyses:{context}"},
        ],
    ).choices[0].message.content
    print("\n=== FINAL (educational only — not financial advice) ===")
    print(decision)


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Top semiconductor stock in Japan"
    trade(q)
