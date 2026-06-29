"""Trusted News Hub — site-scoped news digests over a curated allow-list.

Usage:
    pip install -r requirements.txt
    export ASTRALABS_API_KEY=sk_live_...
    python trusted_news.py business "central bank rate decisions today"

The TRUSTED dict below is an *example* allow-list to show the pattern.
Replace the domains with your own curated list.
"""
from __future__ import annotations

import json
import os
import sys
import requests

API_BASE = os.environ.get("ASTRALABS_API_BASE", "https://api.astralabsai.com/v1")
API_KEY = os.environ.get("ASTRALABS_API_KEY")

# Example allow-list — replace with your own curated providers.
TRUSTED: dict[str, list[str]] = {
    "global":   ["example-globalnews1.com", "example-globalnews2.com"],
    "business": ["example-business1.com", "example-business2.com"],
    "tech":     ["example-tech1.com", "example-tech2.com"],
    "health":   ["example-health1.org", "example-health2.org"],
    "policy":   ["example-policy1.gov", "example-policy2.org"],
    "research": ["example-research1.org", "example-research2.org"],
}


def trusted_news(section: str, topic: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Set ASTRALABS_API_KEY in your environment (see .env.example).")
    if section not in TRUSTED:
        raise ValueError(f"Unknown section '{section}'. Known: {list(TRUSTED)}")
    sites = " OR ".join(f"site:{d}" for d in TRUSTED[section])
    query = f"({sites}) {topic}"
    r = requests.post(
        f"{API_BASE}/insights",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"query": query, "mode": "quick"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    if len(sys.argv) < 3:
        print('Usage: python trusted_news.py <section> "<topic>"')
        print(f"Sections: {', '.join(TRUSTED)}")
        sys.exit(1)
    section = sys.argv[1]
    topic = " ".join(sys.argv[2:])
    data = trusted_news(section, topic)
    print(f"\n=== {section.title()} digest · {topic} ===\n")
    print(data.get("insight") or data.get("summary") or "(no insight returned)")
    print("\nSources:")
    for s in (data.get("sources") or [])[:6]:
        print(f"  - {s.get('title')} -> {s.get('url')}")


if __name__ == "__main__":
    main()
