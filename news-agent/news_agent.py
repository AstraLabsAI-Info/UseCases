"""AI News Agent — summarize the latest news on any topic with cited sources.

Usage:
    export ASTRALABS_API_KEY=sk_live_...
    python news_agent.py "OpenAI"
"""
from __future__ import annotations

import os
import sys
import requests

API_BASE = os.environ.get("ASTRALABS_API_BASE", "https://api.astralabsai.com/v1")
API_KEY = os.environ.get("ASTRALABS_API_KEY")


def news_digest(topic: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Set ASTRALABS_API_KEY in your environment.")
    r = requests.post(
        f"{API_BASE}/insights",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"query": f"latest news about {topic}", "mode": "quick"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    topic = " ".join(sys.argv[1:]) or "OpenAI"
    data = news_digest(topic)
    print(f"\n=== News digest · {topic} ===\n")
    print(data.get("insight") or data.get("summary") or "(no insight returned)")
    print("\nSources:")
    for s in (data.get("sources") or [])[:5]:
        print(f"  - {s.get('title')} -> {s.get('url')}")


if __name__ == "__main__":
    main()
