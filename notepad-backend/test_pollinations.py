import requests
import urllib.parse

prompt = "Hello! Are you working?"
encoded_prompt = urllib.parse.quote(prompt)
url = f"https://text.pollinations.ai/{encoded_prompt}"

print(f"Testing {url}...")
try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
