import sys
import json
import os
import requests

API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
HISTORY_FILE = "inputhistory.json"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Load conversation history
history = []
if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except json.JSONDecodeError:
        history = []

# Read input from stdin
try:
    raw_input = sys.stdin.read()
    user_input = json.loads(raw_input).get("input", "")
    user_input = str(user_input).strip()

    if not user_input:
        raise ValueError("Input is empty or invalid.")
except Exception as e:
    print(f"Input error: {str(e)}", file=sys.stderr)
    sys.exit(1)

# Add to history
history.append({'input': user_input})

# Save history
try:
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
except Exception as e:
    print(f"Error saving history: {str(e)}", file=sys.stderr)

# Prepare payload
payload = {
    "model": "gemma2-9b-it",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
}

# Print payload for debugging
#print("Payload:", json.dumps(payload, indent=2), file=sys.stderr)

# Make request
try:
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    print(result["choices"][0]["message"]["content"])
    print(result["choices"][0]["message"]["content"],file=sys.stderr)
except requests.exceptions.RequestException as e:
    print(json.dumps({
        "error": str(e),
        "status": "error",
        "status_code": getattr(e.response, 'status_code', None),
        "response_text": getattr(e.response, 'text', '')
    }), file=sys.stderr)
    sys.exit(1)