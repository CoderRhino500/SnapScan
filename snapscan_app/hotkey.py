from pynput import keyboard
from config import load_config

def start_listener(callback):
    try:
        config = load_config()
        hotkey_str = config.get("hotkey", "<ctrl>+<f9>")

        mapping = \
        {
            hotkey_str: callback
        }

        listener = keyboard.GlobalHotKeys(mapping)
        return listener
    except Exception as e:
        raise Exception(f"Failed to start hotkey listener: {e}")