"""
Persistent user preference memory for Copilot and dashboard.
"""
import json
import os

PREFS_FILE = "user_prefs.json"

def load_prefs():
    if os.path.exists(PREFS_FILE):
        with open(PREFS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_prefs(prefs):
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f)

def set_pref(key, value):
    prefs = load_prefs()
    prefs[key] = value
    save_prefs(prefs)

def get_pref(key, default=None):
    prefs = load_prefs()
    return prefs.get(key, default)
