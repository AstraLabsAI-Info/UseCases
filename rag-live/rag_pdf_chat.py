"""RAG over one or many PDFs with bring-your-own LLM provider.

Usage:
    pip install -r requirements.txt
    cp .env.example .env   # fill in OPENAI_API_KEY + LLM_API_KEY/BASE_URL
    export $(grep -v '^#' .env | xargs)
    python rag_pdf_chat.py doc1.pdf doc2.pdf

Embeddings use OpenAI (text-embedding-3-small). Chat completion works with any
OpenAI-compatible provider (OpenAI, xAI Grok, Google Gemini, DeepSeek, Qwen,
Moonshot/Kimi). Verify base URLs on the provider's docs.
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field
from typing import List

import pypdf
from openai import OpenAI

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gpt-4o-mini")

embedder = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
llm = OpenAI(
    api_key=os.environ.get("LLM_API_KEY", os.environ["OPENAI_API_KEY"]),
    base_url=os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1"),
)


def chunks_from_pdf(path: str, size: int = 1100, overlap: int = 150) -> List[str]:
    reader = pypdf.PdfReader(path)
    text = "\n".join(p.extract_text() or "" for p in reader.pages)
    out: List[str] = []
    i = 0
    while i < len(text):
        out.append(text[i : i + size])
        i += size - overlap
    return out


def embed(texts: List[str]) -> List[List[float]]:
    r = embedder.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in r.data]


@dataclass
class Chunk:
    doc_title: str
    content: str
    embedding: List[float]
    similarity: float = 0.0


@dataclass
class InMemoryIndex:
    chunks: List[Chunk] = field(default_factory=list)

    def search(self, doc_title: str, query_emb: List[float], k: int = 5) -> List[Chunk]:
        scored: List[Chunk] = []
        for c in self.chunks:
            if c.doc_title != doc_title:
                continue
            sim = _cosine(c.embedding, query_emb)
            scored.append(
                Chunk(c.doc_title, c.content, c.embedding, similarity=sim)
            )
        scored.sort(key=lambda c: c.similarity, reverse=True)
        return scored[:k]


def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb + 1e-9)


def build_index(pdf_paths: List[str]) -> InMemoryIndex:
    idx = InMemoryIndex()
    for path in pdf_paths:
        title = os.path.basename(path)
        pieces = chunks_from_pdf(path)
        if not pieces:
            continue
        vecs = embed(pieces)
        idx.chunks.extend(Chunk(title, p, v) for p, v in zip(pieces, vecs))
        print(f"Indexed {title}: {len(pieces)} chunks")
    return idx


def answer(question: str, idx: InMemoryIndex, top_k_per_doc: int = 5, max_total: int = 10) -> dict:
    q = embed([question])[0]
    doc_titles = sorted({c.doc_title for c in idx.chunks})
    merged: List[Chunk] = []
    for d in doc_titles:
        merged.extend(idx.search(d, q, top_k_per_doc))
    merged.sort(key=lambda c: c.similarity, reverse=True)
    top = merged[:max_total]
    ctx = "\n\n---\n\n".join(
        f"[{i+1}] ({c.doc_title}) {c.content}" for i, c in enumerate(top)
    )
    completion = llm.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": f"Answer ONLY from context, cite as [n].\n\n{ctx}",
            },
            {"role": "user", "content": question},
        ],
    )
    return {
        "answer": completion.choices[0].message.content,
        "citations": [
            {"n": i + 1, "doc_title": c.doc_title, "preview": c.content[:160]}
            for i, c in enumerate(top)
        ],
    }


def main() -> None:
    paths = sys.argv[1:]
    if not paths:
        print("Usage: python rag_pdf_chat.py doc1.pdf [doc2.pdf ...]")
        sys.exit(1)
    idx = build_index(paths)
    print("\nReady. Ask questions (Ctrl+C to quit).")
    try:
        while True:
            q = input("\n> ").strip()
            if not q:
                continue
            out = answer(q, idx)
            print(f"\nAnswer: {out['answer']}")
            print("\nCitations:")
            for c in out["citations"]:
                print(f"  [{c['n']}] {c['doc_title']} — {c['preview']}…")
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
