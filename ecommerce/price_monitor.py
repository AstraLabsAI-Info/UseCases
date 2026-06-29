"""E-commerce price monitor — competitor product listings."""
import os, sys, json, requests
API = os.environ.get('ASTRALABS_API_BASE', 'https://api.astralabsai.com/v1')
KEY = os.environ['ASTRALABS_API_KEY']

def monitor(product: str) -> dict:
    r = requests.post(f"{API}/insights",
        headers={'Authorization': f'Bearer {KEY}'},
        json={'query': f'current prices and listings for: {product}', 'mode': 'quick'},
        timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == '__main__':
    q = ' '.join(sys.argv[1:]) or 'Sony WH-1000XM5 headphones'
    print(json.dumps(monitor(q), indent=2))
