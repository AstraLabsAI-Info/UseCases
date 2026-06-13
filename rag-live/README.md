# RAG + Live Search (PDF Chatbot)

Chat with one or many PDFs — retrieval-augmented answers grounded in
citations. Bring your own LLM (any OpenAI-compatible provider: OpenAI,
Gemini, Grok, DeepSeek, etc.).

🔗 Live demo: <https://www.astralabsai.com/examples/rag-live>

## What it does

1. Extract text from one or more PDFs (`pypdf`).
2. Chunk the text (≈1100 chars, 150 overlap).
3. Embed chunks with `text-embedding-3-small`.
4. At query time: embed the question, top-k vector search per document,
   merge results, send to your chat model with strict "answer from context
   only, cite as [n]" instructions.

The included `rag_pdf_chat.py` uses an in-memory cosine-similarity index so
you can run it stand-alone. Swap `InMemoryIndex` for pgvector, Pinecone,
Qdrant, etc. for production.

## Requirements

- Python 3.9+
- An OpenAI key (used for embeddings)
- Any OpenAI-compatible chat LLM key

## Setup

```bash
pip install -r requirements.txt

# Embeddings (uses OpenAI text-embedding-3-small)
export OPENAI_API_KEY=sk-...

# Chat LLM (bring your own provider)
export LLM_API_KEY=sk-...
export LLM_BASE_URL=https://api.openai.com/v1       # or DeepSeek, Gemini OpenAI shim, ...
export CHAT_MODEL=gpt-4o-mini
```

## Run

```bash
python rag_pdf_chat.py path/to/doc1.pdf path/to/doc2.pdf
```

Then type questions at the prompt:

```
> What does the paper say about scaling laws?
Answer: ... [1][2]
Citations:
  [1] doc1.pdf — "..."
  [2] doc2.pdf — "..."
```

## Use as a library

```python
from rag_pdf_chat import build_index, answer
idx = build_index(["doc1.pdf", "doc2.pdf"])
print(answer("Summarize the conclusion", idx))
```
