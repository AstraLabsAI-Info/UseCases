"""Streamlit UI for the LangChain / MCP agent example."""
import streamlit as st

from agent import build_executor

st.set_page_config(page_title="LangChain Agent", page_icon="🧠")
st.title("🧠 LangChain Agent + AstraLabsAI tool")
st.caption("The LLM decides when to call astralabs_search for live evidence.")

if "executor" not in st.session_state:
    st.session_state.executor = build_executor()

q = st.text_input("Question", value="Who recently raised funding in the AI search space?")
if st.button("Run agent", type="primary", disabled=not q.strip()):
    with st.spinner("Agent working..."):
        result = st.session_state.executor.invoke({"input": q.strip()})
    st.subheader("Answer")
    st.write(result.get("output", result))
