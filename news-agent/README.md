# AI News Agent

Fetch real-time news on any topic and get a summarized digest with cited
sources. Uses the AstraLabsAI `/v1/insights` endpoint — no LLM key required;
the API returns a summary plus the sources it used.

🔗 Live demo: <https://www.astralabsai.com/examples/news-agent>

## What it does

Given a topic (e.g. `"OpenAI"`), the script calls `POST /v1/insights` in
`quick` mode and prints:

- A natural-language news digest
- The top sources (title + URL) used to produce it

## Requirements

- Python 3.9+
- An AstraLabsAI API key

## Setup

```bash
pip install -r requirements.txt
export ASTRALABS_API_KEY=sk_live_...
```

## Run

```bash
python news_agent.py
# or with a custom topic
python news_agent.py "AI search startups"
```

## Expected output

```
Insight: OpenAI announced ...
- "OpenAI ships ..." -> https://...
- "Sam Altman on ..." -> https://...
```

## Use as a library

```python
from news_agent import news_digest
data = news_digest("AI search startups")
print(data["insight"])
for s in data["sources"][:5]:
    print(s["title"], "->", s["url"])
```

## Alternative languages

A Node.js (built-in `fetch`) port and a `curl` one-liner are documented on the
live demo page.
