import urllib.request
import urllib.error

pages = [
    ('/', 'Home'),
    ('/detector/', 'Detector'),
    ('/analytics/', 'Analytics'),
]

for url, name in pages:
    try:
        resp = urllib.request.urlopen(f'http://127.0.0.1:8000{url}')
        print(f"✓ {name:15} - Success (Status: {resp.status})")
    except urllib.error.HTTPError as e:
        print(f"✗ {name:15} - Error {e.code}")
    except Exception as e:
        print(f"✗ {name:15} - {type(e).__name__}: {str(e)[:50]}")
