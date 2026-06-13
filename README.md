# AstraLabsAI — Code Examples

Runnable reference implementations for each demo on
[astralabsai.com/examples](https://www.astralabsai.com). Every folder is a
self-contained mini-project that you can copy into a fresh repo and push to
GitHub.

| Example | What it shows |
| --- | --- |
| [`news-agent/`](./news-agent) | Pull real-time, cited news on any topic via `POST /v1/insights`. |
| [`market-intel/`](./market-intel) | Turn live web evidence into structured market-intelligence JSON with an LLM of your choice. |
| [`rag-live/`](./rag-live) | RAG over one or many PDFs with bring-your-own LLM (OpenAI / Gemini / Grok / DeepSeek …). |
| [`langchain-mcp/`](./langchain-mcp) | A LangChain tool-calling agent (also reusable as an MCP tool) that calls `astralabs_search`. |
| [`trading-agents/`](./trading-agents) | **Educational only.** Multi-agent equity-research desk over any world market. Not financial advice. |

## Prerequisites

All examples expect an AstraLabsAI API key:

```bash
export ASTRALABS_API_KEY=sk_live_...   # or sk_test_...
```

Get one from your dashboard at `https://www.astralabsai.com/dashboard`.

The API base URL is:

```
https://api.astralabsai.com/v1
```

## Running an example

```bash
cd examples/news-agent
pip install -r requirements.txt
python news_agent.py
```

Each folder's own `README.md` documents the required environment variables,
install steps, expected output, and what to customize.

## License

These examples are provided under the MIT license — see the LICENSE file in
each subfolder. You're free to copy them into your own projects.
