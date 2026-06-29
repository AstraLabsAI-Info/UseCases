"""Streamlit UI for the RAG + Live Search PDF chatbot."""
import os
import tempfile
import streamlit as st

from rag_pdf_chat import build_index, answer

st.set_page_config(page_title="RAG PDF Chat", page_icon="📚")
st.title("📚 RAG PDF Chat")
st.caption("Chat with one or more PDFs — answers grounded in citations.")

uploads = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if "idx" not in st.session_state:
    st.session_state.idx = None

if st.button("Build index", disabled=not uploads):
    paths = []
    tmp = tempfile.mkdtemp()
    for f in uploads:
        p = os.path.join(tmp, f.name)
        with open(p, "wb") as out:
            out.write(f.read())
        paths.append(p)
    with st.spinner("Embedding chunks..."):
        st.session_state.idx = build_index(paths)
    st.success(f"Indexed {len(paths)} PDF(s).")

q = st.text_input("Question", value="Summarize the conclusion")
if st.button("Ask", type="primary", disabled=not (st.session_state.idx and q.strip())):
    with st.spinner("Thinking..."):
        out = answer(q.strip(), st.session_state.idx)
    st.subheader("Answer")
    st.write(out["answer"])
    st.markdown("**Citations**")
    for c in out["citations"]:
        st.markdown(f"- **[{c['n']}] {c['doc_title']}** — {c['preview']}…")
