"""Healthcare literature search — cited summaries. Not medical advice."""
import os, sys, json, requests
API = os.environ.get('ASTRALABS_API_BASE', 'https://api.astralabsai.com/v1')
KEY = os.environ['ASTRALABS_API_KEY']

def search(question: str) -> dict:
    r = requests.post(f"{API}/insights",
        headers={'Authorization': f'Bearer {KEY}'},
        json={'query': f'peer-reviewed medical literature on: {question} - cite studies', 'mode': 'quick'},
        timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == '__main__':
    q = ' '.join(sys.argv[1:]) or 'GLP-1 agonists for weight loss'
    print(json.dumps(search(q), indent=2))
