# AI Agents — LangChain / MCP

A real tool-calling agent: an LLM decides when to call the
`astralabs_search` tool, runs it against the AstraLabsAI live-web API,
reasons over the results, and answers. The same tool shape works in
LangChain, OpenAI tools, or any MCP-compatible host.

🔗 Live demo: <https://www.astralabsai.com/examples/langchain-mcp>

## Two ways to use it

| File | What it is |
| --- | --- |
| `agent.py` | LangChain agent using `create_openai_tools_agent` + `AgentExecutor`. |
| `mcp_tool.ts` | TypeScript MCP tool definition you can register with any MCP host. |

## Requirements

- Python 3.9+ (for `agent.py`)
- Node 18+ (for `mcp_tool.ts`)
- AstraLabsAI API key (the agent's tool)
- OpenAI-compatible LLM key (drives the agent)

## Setup (Python / LangChain)

```bash
pip install -r requirements.txt
export ASTRALABS_API_KEY=sk_live_...
export OPENAI_API_KEY=sk-...
```

## Run

```bash
python agent.py "Who recently raised funding in the AI search space?"
```

Verbose mode is on — you'll see the agent decide to call `astralabs_search`,
the tool's JSON result, and the final answer.

## MCP host integration (TypeScript)

```ts
import { astralabsSearchTool } from "./mcp_tool";
// Register the tool with your MCP server / OpenAI tools runtime.
```

The tool's input schema (`{ query: string }`) and output (JSON from
`/v1/insights`) are stable — no LangChain dependency required.
