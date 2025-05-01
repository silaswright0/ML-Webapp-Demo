import sys
import json
import os
import requests

API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
HISTORY_FILE = "inputhistory.json"
RESPONSES_FILE = "responseshistory.json"

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
        
responses = []
if os.path.exists(RESPONSES_FILE):
    try:
        with open(RESPONSES_FILE, 'r') as f:
            responses = json.load(f)
    except json.JSONDecodeError:
        responses = []

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

messages = [
    {"role": "system", "content": """You are a helpful assistant. Based on user input, generate only JavaScript code that draws onto the HTML canvas below. 
                                            Do not add any HTML, explanations, or extra text. Only generate JavaScript code. The canvas is already defined as:
                                            <div class="frame">
                                            <canvas id="mainCanvas" width="800" height="600"></canvas>
                                            </div>
                                            Assume you have access to the canvas context (ctx) already initialized as:
                                            const ctx = document.getElementById('mainCanvas').getContext('2d');
    """}
]
#add to message list
for i,entry in enumerate(history):
    messages.append({"role": "user", "content": entry["input"]})
    #print(entry["input"],file=sys.stderr)
    if i < len(responses):
        responseContent = responses[i]['response']['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": responseContent})
        #print(responses[i]["response"],file=sys.stderr)

#print(messages,file=sys.stderr)

# Prepare payload
payload = {
    "model": "gemma2-9b-it",
    "messages": messages,
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
    responses.append({'response':result})
    #print(result["choices"][0]["message"]["content"],file=sys.stderr)
    print(json.dumps({"text": result["choices"][0]["message"]["content"]}))
except requests.exceptions.RequestException as e:
    print(json.dumps({
        "error": str(e),
        "status": "error",
        "status_code": getattr(e.response, 'status_code', None),
        "response_text": getattr(e.response, 'text', '')
    }), file=sys.stderr)
    sys.exit(1)

#save responses
try:
    with open(RESPONSES_FILE, 'w') as f:
        json.dump(responses, f, indent=2)
except Exception as e:
    print(f"Error saving responses: {str(e)}", file=sys.stderr)