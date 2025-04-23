import sys
import json
import os

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

response = " "#this is where magic happens :)

#notes:
# -use ML deepseek? to generate html for the canvas
# -save previous responses in some data structure so small tweaks can be inputed
# -restructure input into some series of prompts, do prompt research!!!

print(json.dumps(response))