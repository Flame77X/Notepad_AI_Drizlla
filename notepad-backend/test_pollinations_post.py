import requests

prompt = "This is a test prompt sent via POST to verify I can send longer context."
print(f"Testing POST to https://text.pollinations.ai/ ...")
try:
    response = requests.post("https://text.pollinations.ai/", data=prompt, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
