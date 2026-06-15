import urllib.request
import json

data = json.dumps({"email": "test@error.com", "password": "pass"}).encode('utf-8')
req = urllib.request.Request("http://127.0.0.1:8000/api/auth/register", data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()}")
