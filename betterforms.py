'''
import sys
import json
import os
#Deepseek API setup below
import requests

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-1854e779ca824e23b6846bc79b653439"  

headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}

data = {
    "model": "deepseek-coder",
    "messages": [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    "temperature": 0.7,
    "max_tokens": 1024,
}

# data structure for input history
history = []
filename = "inputhistory.json"

if os.path.exists(filename):
    with open(filename,'r') as f:
        history = json.load(f)

# Read input from Node.js
raw_input = sys.stdin.read()
data = json.loads(raw_input)
user_input = data.get('input', '')

history.append({'input':user_input})

with open(filename,'w') as f:
    json.dump(history,f,indent=2)

#for item in history:
#    print(item['input'],file=sys.stderr)

r = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)

if r.status_code == 200:
    response = r.json()["choices"][0]["message"]["content"]
    print(response,file=sys.stderr)
else:
    print(f"Error: {r.status_code}, {r.text}",file=sys.stderr)

#notes:
# -use ML deepseek? to generate html for the canvas
# -save previous responses in some data structure so small tweaks can be inputed
# -restructure input into some series of prompts, do prompt research!!!
'''
'''
import sys
import json
import os
import requests

# Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"
HISTORY_FILE = "inputhistory.json"

# Initialize headers
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

# Read input from Node.js
try:
    raw_input = sys.stdin.read()
    user_input = json.loads(raw_input).get('input', '')
    user_input = str(user_input)
except Exception as e:
    print(f"Error reading input: {str(e)}", file=sys.stderr)
    sys.exit(1)

# Add to history
history.append({'input': user_input})

# Prepare API payload
payload = {
    "model": "mixtral-8x7b-32768",
    "messages": [
        {"role": "system", "content": "You are a helpful AI assistant."},
        #*[{"role": "user", "content": item['input']} for item in history[-5:]],  # Last 5 inputs
        {"role": "user", "content": user_input}
    ],
    "temperature": 0.7,
    "max_tokens": 1024,
}

# Save history
try:
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
except Exception as e:
    print(f"Error saving history: {str(e)}", file=sys.stderr)

# Make API request
# Make API request to Groq
try:
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raises exception for HTTP errors
    
    ai_response = response.json()["choices"][0]["message"]["content"]
    print(json.dumps({
        "response": ai_response,
        "status": "success"
    }))
    
except requests.exceptions.RequestException as e:
    print(json.dumps({
        "error": str(e),
        "status": "error",
        "status_code": getattr(e.response, 'status_code', None)
    }), file=sys.stderr)
    sys.exit(1)
    '''
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