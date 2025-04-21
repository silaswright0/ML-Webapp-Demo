import sys
import json

# Read input from Node.js
raw_input = sys.stdin.read()
data = json.loads(raw_input)
user_input = data.get('input', '')

response = " "#this is where magic happens :)

print(json.dumps(response))