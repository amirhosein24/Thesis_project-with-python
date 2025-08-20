import json, os
BASE = os.path.join(os.path.dirname(__file__), "..", "data")
def load(filename):
    path = os.path.join(BASE, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
def save(filename, data):
    path = os.path.join(BASE, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)