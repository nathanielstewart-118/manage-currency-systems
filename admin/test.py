import json

import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up two levels to the parent of parent directory
config_path = os.path.join(current_dir, "..", "config.json")

# Open and print the config file
with open(config_path, "r") as f:
    config = json.load(f)
print(config)
