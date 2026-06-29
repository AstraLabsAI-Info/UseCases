"""Streamlit UI for the Market Intelligence example."""
import json
import streamlit as st

from market_intel import market_intel

st.set_page_config(page_title="Market Intelligence", page_icon="📊")
st.title("📊 Market Intelligence")
st.caption("Structured JSON market signals from live-web evidence.")

topic = st.text_input("Topic", value="electric vehicles")

if st.button("Run", type="primary", disabled=not topic.strip()):
    with st.spinner("Gathering evidence and structuring signals..."):
        try:
            out = market_intel(topic.strip())
        except Exception as e:
            st.error(str(e))
            st.stop()
    st.subheader("Signals")
    st.json(out.get("signals", {}))
    sources = out.get("sources") or []
    if sources:
        st.markdown("**Sources**")
        for i, s in enumerate(sources[:8], 1):
            st.markdown(f"{i}. [{s.get('title')}]({s.get('url')})")
