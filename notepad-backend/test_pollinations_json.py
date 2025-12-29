import requests

payload = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Can you accept JSON?"}
    ],
    "model": "openai"
}

print(f"Testing POST JSON to https://text.pollinations.ai/ ...")
try:
    response = requests.post("https://text.pollinations.ai/", json=payload, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
