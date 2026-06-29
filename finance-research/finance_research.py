"""Finance research — pull cited news and structured signals for a ticker.
Educational only — not financial advice.
"""
import os, sys, json, requests

API = os.environ.get('ASTRALABS_API_BASE', 'https://api.astralabsai.com/v1')
KEY = os.environ['ASTRALABS_API_KEY']

def research(symbol: str) -> dict:
    r = requests.post(f"{API}/insights",
        headers={'Authorization': f'Bearer {KEY}'},
        json={'query': f'latest news, filings, and analyst views on {symbol}', 'mode': 'quick'},
        timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == '__main__':
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    print(json.dumps(research(symbol), indent=2))
