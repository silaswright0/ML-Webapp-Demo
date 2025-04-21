import sys
import json

# Read input from Node.js
raw_input = sys.stdin.read()
data = json.loads(raw_input)

user_input = data.get('input', '')
response = f'You typed: {user_input}'

print(json.dumps(response))