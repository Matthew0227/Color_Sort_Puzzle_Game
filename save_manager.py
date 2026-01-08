import json
import os

SAVE_FILE = "save.json"

DEFAULT_SAVE = {
    "level_unlocked": 1,
    "stars": {},
    "settings": {
        "music": True,
        "volume": 0.6
    }
}

def load_save():
    if not os.path.exists(SAVE_FILE):
        save_game(DEFAULT_SAVE)
        return DEFAULT_SAVE.copy()

    with open(SAVE_FILE, "r") as f:
        return json.load(f)

def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
