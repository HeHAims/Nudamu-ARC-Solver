import json
import os

def secure_load_json(filename):
    if not filename.endswith('.json'):
        raise ValueError("Only .json files are allowed.")
    safe_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(safe_dir, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Secure file not found: {filename}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
