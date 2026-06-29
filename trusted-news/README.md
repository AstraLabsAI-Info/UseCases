# Trusted News Hub Agent

Run targeted news queries scoped to your own curated allow-list of trusted
news providers — picked per section (Global, Business, Tech, Health, Policy,
Research). Every result is constrained to the allow-listed domains so you
control the source of truth.

🔗 Live demo: <https://www.astralabsai.com/examples/trusted-news>

> The provider domains in this example are illustrative samples to show how
> the allow-listing works — they are **not** endorsements or partnerships.
> Replace them with your own curated list.

## What it does

Given a `section` (e.g. `business`) and a `topic`, the script builds a
`site:` filter from that section's allow-list and posts it to
`POST /v1/insights`:

```
(site:example1.com OR site:example2.com OR site:example3.com) <topic>
```

The API returns a summarized digest plus the cited sources — all guaranteed
to come from your allow-listed domains.

## Requirements

- Python 3.9+
- An AstraLabsAI API key
- (Optional) Streamlit, for the included UI

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# then edit .env to add your ASTRALABS_API_KEY
```

## Run (CLI)

```bash
export $(cat .env | xargs)
python trusted_news.py business "central bank rate decisions today"
```

## Run (Streamlit UI)

```bash
export $(cat .env | xargs)
streamlit run streamlit_app.py
```

Pick a section, type a topic, and the UI calls the same `trusted_news()`
helper used by the CLI.

## Customize the allow-list

Open `trusted_news.py` and edit the `TRUSTED` dict — add or remove sections,
add or remove domains. The script does the rest.
