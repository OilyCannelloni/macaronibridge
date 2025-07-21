import json
import os

def load_config(filename="config.json"):
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, filename)
    
    with open(config_path, "r") as file:
        return json.load(file)

config = load_config()
