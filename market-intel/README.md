# Market Intelligence

Track industries, supply chains, and pricing signals across the live web —
then turn that evidence into structured JSON with an LLM of your choice.

🔗 Live demo: <https://www.astralabsai.com/examples/market-intel>

## How it works

1. Call `POST /v1/insights` to pull cited evidence about a topic.
2. Send the evidence to an OpenAI-compatible LLM (OpenAI, Gemini, Grok,
   DeepSeek, …) with `response_format={"type":"json_object"}`.
3. Get back a structured dict: `headline`, `key_players`, `pricing_signals`,
   `supply_chain_signals`, `growth_drivers`, `risks`.

## Requirements

- Python 3.9+
- AstraLabsAI API key
- An OpenAI-compatible LLM key (defaults to OpenAI `gpt-4o-mini`)

## Setup

```bash
pip install -r requirements.txt
export ASTRALABS_API_KEY=sk_live_...
export OPENAI_API_KEY=sk-...
```

To use a different OpenAI-compatible provider, point the OpenAI SDK at
another base URL:

```bash
export OPENAI_API_KEY=...           # your provider's key
export OPENAI_BASE_URL=https://api.deepseek.com/v1
export LLM_MODEL=deepseek-chat
```

## Run

```bash
python market_intel.py "electric vehicles"
```

## Expected output

```json
{
  "topic": "electric vehicles",
  "signals": {
    "headline": "...",
    "key_players": [...],
    "pricing_signals": [...],
    "supply_chain_signals": [...],
    "growth_drivers": [...],
    "risks": [...]
  },
  "sources": [...]
}
```
