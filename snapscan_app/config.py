import json
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        default_config = \
        {
            "hotkey": "<ctrl>+<f9>",
            "notification_duration": 3,
            "auto_open_urls": True,
            "monitor": 1,
            "save_history": False,
            "url_validation": True
        }
        save_config(default_config)
        return default_config
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return \
        {
        }

def save_config(config):
    config_path = Path(__file__).parent / "config.json"
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")