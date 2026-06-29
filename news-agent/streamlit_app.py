"""Streamlit UI for the AI News Agent example.

Run:
    pip install -r requirements.txt
    export ASTRALABS_API_KEY=sk_live_...
    streamlit run streamlit_app.py
"""
import streamlit as st

from news_agent import news_digest

st.set_page_config(page_title="AI News Agent", page_icon="📰")
st.title("📰 AI News Agent")
st.caption("Real-time news digest with cited sources, via AstraLabsAI /v1/insights.")

topic = st.text_input("Topic", value="AI search startups")

if st.button("Get digest", type="primary", disabled=not topic.strip()):
    with st.spinner("Fetching live news..."):
        try:
            data = news_digest(topic.strip())
        except Exception as e:
            st.error(str(e))
            st.stop()
    st.subheader("Digest")
    st.write(data.get("insight") or data.get("summary") or "_(no insight)_")
    sources = data.get("sources") or []
    if sources:
        st.markdown("**Sources**")
        for i, s in enumerate(sources[:8], 1):
            st.markdown(f"{i}. [{s.get('title')}]({s.get('url')})")
