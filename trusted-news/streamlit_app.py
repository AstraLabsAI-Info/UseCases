"""Streamlit UI for the Trusted News Hub example.

Run:
    pip install -r requirements.txt
    export ASTRALABS_API_KEY=sk_live_...
    streamlit run streamlit_app.py
"""
import streamlit as st

from trusted_news import TRUSTED, trusted_news

st.set_page_config(page_title="Trusted News Hub", page_icon="🛡️")
st.title("🛡️ Trusted News Hub")
st.caption("Site-scoped news digests over your curated allow-list of providers.")

section = st.selectbox("Section", list(TRUSTED.keys()))
topic = st.text_input("Topic", value="top headlines today")

if st.button("Run", type="primary", disabled=not topic.strip()):
    with st.spinner("Querying trusted providers..."):
        try:
            data = trusted_news(section, topic.strip())
        except Exception as e:
            st.error(str(e))
            st.stop()

    st.subheader(f"{section.title()} digest")
    st.write(data.get("insight") or data.get("summary") or "_(no insight)_")
    sources = data.get("sources") or []
    if sources:
        st.markdown("**Sources**")
        for i, s in enumerate(sources[:8], 1):
            st.markdown(f"{i}. [{s.get('title')}]({s.get('url')}) — _{s.get('source')}_")
