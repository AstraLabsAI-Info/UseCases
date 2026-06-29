"""Streamlit UI for the Trading Agents demo. Educational only — not financial advice."""
import io
import contextlib
import streamlit as st

from trading_agents import trade

st.set_page_config(page_title="Trading Agents (Educational)", page_icon="📈")
st.title("📈 Trading Agents Demo")
st.warning("Educational demo only. Not financial advice.")

q = st.text_input("Research prompt", value="Top semiconductor stock in Japan")
if st.button("Run desk", type="primary", disabled=not q.strip()):
    buf = io.StringIO()
    with st.spinner("Specialists deliberating..."), contextlib.redirect_stdout(buf):
        try:
            trade(q.strip())
        except Exception as e:
            st.error(str(e))
            st.stop()
    st.code(buf.getvalue(), language="markdown")
