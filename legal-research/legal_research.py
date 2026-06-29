"""Legal research — cited statute and case-law lookup. Not legal advice."""
import os, sys, json, requests
API = os.environ.get('ASTRALABS_API_BASE', 'https://api.astralabsai.com/v1')
KEY = os.environ['ASTRALABS_API_KEY']

def research(question: str, jurisdiction: str = 'US') -> dict:
    r = requests.post(f"{API}/insights",
        headers={'Authorization': f'Bearer {KEY}'},
        json={'query': f'{question} (jurisdiction: {jurisdiction}) - cite statutes and cases', 'mode': 'quick'},
        timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == '__main__':
    q = ' '.join(sys.argv[1:]) or 'GDPR data retention'
    print(json.dumps(research(q), indent=2))
