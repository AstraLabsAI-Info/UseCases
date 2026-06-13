# Trading Agents Demo (Multi-Agent)

> ⚠️ **Educational demo only — NOT financial advice.**
> This example shows how to wire a multi-agent AI pipeline using
> AstraLabsAI as the live-web tool. Do not use any output for real
> trading decisions. You are solely responsible for your own investments.

A team of specialist agents — Market Analyst, News & Sentiment Analyst, Bull
Researcher, Bear Researcher, Risk Manager, and Head Trader — debate a ticker
and produce a structured recommendation. A "resolver" step first turns a
free-form English question (e.g. *"top semiconductor stock in Japan"*) into
an exchange-qualified ticker on any world market.

🔗 Live demo: <https://www.astralabsai.com/examples/trading-agents>

## Requirements

- Python 3.9+
- AstraLabsAI API key (live-web tool)
- OpenAI-compatible LLM key (drives every agent)

## Setup

```bash
pip install -r requirements.txt
export ASTRALABS_API_KEY=sk_live_...
export OPENAI_API_KEY=sk-...
```

To use a different OpenAI-compatible provider (DeepSeek, Gemini OpenAI
shim, Grok, etc.):

```bash
export OPENAI_BASE_URL=https://api.deepseek.com/v1
export LLM_MODEL=deepseek-chat
```

## Run

```bash
python trading_agents.py "Top semiconductor stock in Japan"
python trading_agents.py "Largest EV maker listed in China"
python trading_agents.py "NVDA"
```

## What it prints

1. **Resolved ticker** (e.g. `7203.T` — Toyota Motor Corp · TSE · JPY)
2. Each agent's analysis, with the live-web searches they performed
3. **FINAL JSON** from the Head Trader:

```json
{
  "action": "HOLD",
  "confidence": 55,
  "horizon": "3-6 months",
  "thesis": "...",
  "key_risks": ["..."],
  "catalysts": ["..."]
}
```

## Disclaimer (please read)

This code is provided strictly for learning how multi-agent LLM systems
work. It is **not investment advice**, not a recommendation to buy or sell
any security, and not a substitute for a licensed financial advisor.
Markets carry risk; past performance does not guarantee future results.
