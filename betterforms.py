import json
import random

# You can later pull real data or use ML logic here
response = {
    "text": "Dynamic Canvas!",
    "color": random.choice(["red", "green", "blue", "purple"])
}

print(json.dumps(response))