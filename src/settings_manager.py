import json
import os

SETTINGS_FILE = "settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "appearance_mode": "dark",
    "preview_page_size": "medium",
    "default_save_path": os.path.expanduser("~/Documents")
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)
