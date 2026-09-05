import requests
import json

# Make a prediction to populate history
urls = [
    'http://example.com',
    'http://google.com',
    'http://suspicious-bank-login.com',
    'http://github.com'
]

for url in urls:
    try:
        response = requests.post('http://127.0.0.1:5000/api/predict', json={'url': url})
        if response.status_code == 200:
            result = response.json()
            print(f"Tested {url}: {result.get('result', 'Unknown')}")
        else:
            print(f"Failed {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Error with {url}: {e}")

# Check if history has entries
try:
    r = requests.get('http://127.0.0.1:5000/api/history')
    if r.status_code == 200:
        history = r.json()
        print(f"\nTotal history entries: {len(history['history'])}")
except Exception as e:
    print(f"Error fetching history: {e}")

# Test the trends endpoint
try:
    r = requests.get('http://127.0.0.1:5000/api/statistics')
    if r.status_code == 200:
        stats = r.json()
        print(f"Stats: Phishing={stats.get('phishing')}, Legit={stats.get('legit')}")
except Exception as e:
    print(f"Error fetching stats: {e}")
