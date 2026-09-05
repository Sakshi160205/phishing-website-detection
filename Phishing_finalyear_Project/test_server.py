import urllib.request
import urllib.error

try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000/detector/')
    print("Success! Status:", resp.status)
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    try:
        error_html = e.read().decode()
        # Extract error message
        import re
        match = re.search(r'<h1>([^<]+)</h1>', error_html)
        if match:
            print("Error:", match.group(1))
        match = re.search(r'<p>([^<]+)</p>', error_html)
        if match:
            print("Details:", match.group(1)[:200])
    except:
        pass
