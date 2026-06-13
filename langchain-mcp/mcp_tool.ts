// MCP-style tool definition. Register with any MCP-compatible host or use
// directly as an OpenAI tools function.
//
// Env:
//   ASTRALABS_API_KEY  (required)
//   ASTRALABS_API_BASE (optional, defaults to https://api.astralabsai.com/v1)

const API_BASE = process.env.ASTRALABS_API_BASE ?? "https://api.astralabsai.com/v1";

export const astralabsSearchTool = {
  name: "astralabs_search",
  description: "Search the live web with AstraLabsAI and return cited summaries.",
  inputSchema: {
    type: "object",
    properties: { query: { type: "string" } },
    required: ["query"],
  },
  async execute({ query }: { query: string }) {
    const r = await fetch(`${API_BASE}/insights`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.ASTRALABS_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query, mode: "quick" }),
    });
    if (!r.ok) throw new Error(`astralabs_search failed: ${r.status} ${await r.text()}`);
    return r.json();
  },
};
