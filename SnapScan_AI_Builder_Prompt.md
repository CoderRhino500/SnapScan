# SnapScan — AI Builder Prompt

Use this document as a complete specification to build SnapScan. Follow every instruction exactly. Do not make assumptions or substitute libraries unless explicitly told to.

---

## What You Are Building

A lightweight, cross-platform desktop application called **SnapScan**. When the user presses a global hotkey, the app takes a screenshot, scans it for a QR code, and opens the detected URL in the user's default browser. The app runs silently in the system tray with no visible window.

It must work on **Windows, macOS, and Linux** without any code changes between platforms.

---

## Core Requirements

- No login, sign-in, or internet connection required
- No data ever leaves the user's computer
- Must run comfortably on machines with 2GB RAM
- Must be as lightweight as possible — avoid heavy dependencies
- All processing happens locally in memory
- Screenshots must never be saved to disk

---

## Exact Libraries to Use

Install with:
```bash
pip install mss pyzbar pynput pystray plyer Pillow
```

| Library | Version Constraint | Purpose |
|---|---|---|
| `mss` | Latest | Screenshot capture |
| `pyzbar` | Latest | QR code decoding |
| `Pillow` | Latest | Image format conversion |
| `pynput` | Latest | Global hotkey listener |
| `pystray` | Latest | System tray icon |
| `plyer` | Latest | Toast notifications |
| `webbrowser` | Built-in | Open URLs in browser |
| `threading` | Built-in | Run tray + hotkey simultaneously |
| `pathlib` | Built-in | Cross-platform file paths |
| `json` | Built-in | Config file handling |

**Do NOT use:**
- `opencv-python` (too heavy — use Pillow instead)
- `keyboard` (requires root on Linux — use pynput instead)
- `win10toast` (Windows only — use plyer instead)
- `infi.systray` (Windows only — use pystray instead)
- Any cloud APIs or external services

---

## Exact Project Structure

Create every file listed below. Do not add extra files or rename any of them.

```
SnapScan/
│
├── main.py              # Entry point — ties everything together
├── hotkey.py            # Global hotkey listener logic
├── screenshot.py        # Screenshot capture and image conversion
├── scanner.py           # QR code decoding logic
├── notifier.py          # Toast notification logic
├── tray.py              # System tray icon and menu
├── config.py            # Config loading and saving
│
├── config.json          # Default user configuration
├── requirements.txt     # pip dependencies
├── icon.png             # Placeholder tray icon (generate a simple one)
├── LICENSE              # LGPL v3 License text
└── README.md            # Brief user-facing readme
```

---

## File-by-File Specifications

### config.json
This is the default configuration file. Create it with these exact defaults:

```json
{
  "hotkey": "<ctrl>+<f9>",
  "notification_duration": 3,
  "auto_open_urls": true,
  "monitor": 1,
  "save_history": false,
  "url_validation": true
}
```

---

### config.py
- Load `config.json` from the same directory as the script using `pathlib`
- If `config.json` does not exist, create it with the defaults above
- Expose a single `load_config()` function that returns the config as a dict
- Expose a `save_config(config)` function that writes changes back to `config.json`

```python
# Expected interface
from config import load_config, save_config

config = load_config()
print(config['hotkey'])  # e.g. "<ctrl>+<f9>"
```

---

### screenshot.py
- Use `mss` to capture the screen
- Read the monitor index from config (default: 1 = primary monitor)
- Convert the `mss` screenshot to a **Pillow PIL Image** using this exact method:

```python
from PIL import Image

img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
```

- Expose a single `capture()` function that returns a PIL Image
- Wrap in try/except and raise a descriptive exception on failure
- Do NOT save the screenshot to disk at any point

```python
# Expected interface
from screenshot import capture

image = capture()  # Returns a PIL Image object
```

---

### scanner.py
- Use `pyzbar.pyzbar.decode()` to scan the PIL Image
- Return a dict with the following structure:

```python
# If QR code found:
{
    'found': True,
    'data': 'https://example.com',  # decoded string
    'type': 'QRCODE',               # barcode type
    'rect': (x, y, width, height)   # position on screen
}

# If nothing found:
{
    'found': False
}
```

- Handle `UnicodeDecodeError` if the QR contains binary data (non-text)
- If multiple QR codes are detected, return only the first one
- Expose a single `scan(image)` function

```python
# Expected interface
from scanner import scan

result = scan(image)
if result['found']:
    print(result['data'])
```

---

### notifier.py
- Use `plyer.notification` to show toast notifications
- Always use "SnapScan" as the app name and title
- Read `notification_duration` from config
- Expose a single `notify(message)` function
- Wrap in try/except — if notification fails, fail silently (do not crash the app)

```python
# Expected interface
from notifier import notify

notify("Opening: https://example.com")
notify("No QR code detected")
notify("QR code contains non-URL data: Hello World")
```

---

### hotkey.py
- Use `pynput.keyboard.GlobalHotKeys` to listen for the hotkey
- Read the hotkey combination from config
- Expose a `start_listener(callback)` function that:
  - Registers the hotkey from config
  - Calls `callback()` when the hotkey is pressed
  - Returns the `GlobalHotKeys` instance so it can be started in a thread
- Do NOT block inside this function

```python
# Expected interface
from hotkey import start_listener

def on_hotkey():
    # scan flow goes here
    pass

listener = start_listener(on_hotkey)
```

---

### tray.py
- Use `pystray` to create the system tray icon
- Load the icon from `icon.png` using `pathlib` (never hardcode the path)
- The right-click menu must include:
  - "SnapScan" as a non-clickable title label
  - "Scan Now" — manually triggers the scan callback
  - "Quit" — stops the tray icon and exits the app
- Expose a `create_tray(scan_callback)` function that returns a `pystray.Icon` instance
- The tray icon must NOT start running inside this function — just create and return it

```python
# Expected interface
from tray import create_tray

tray = create_tray(on_scan_triggered)
tray.run()  # Called from main.py
```

---

### main.py
This is the entry point. It must:

1. Load config using `load_config()`
2. Define the main scan function `on_scan_triggered()` which:
   - Calls `capture()` from screenshot.py
   - Passes the image to `scan()` from scanner.py
   - Handles the result:
     - If `found` is True and data is a URL (`http://` or `https://` or `www.`): call `webbrowser.open(url)` and `notify(f"Opening: {url}")`
     - If `found` is True but data is not a URL: call `notify(f"QR code contains: {data}")`
     - If `found` is False: call `notify("No QR code detected")`
   - Wrap everything in try/except and call `notify(f"Error: {e}")` on failure
3. Start the hotkey listener in a **daemon thread** using `threading.Thread`
4. Create the tray icon using `create_tray(on_scan_triggered)`
5. Run the tray icon on the **main thread** (blocking call)

```python
# Expected structure of main.py

import threading
import webbrowser
from config import load_config
from screenshot import capture
from scanner import scan
from notifier import notify
from hotkey import start_listener
from tray import create_tray

def main():
    config = load_config()

    def on_scan_triggered():
        try:
            image = capture()
            result = scan(image)
            # handle result here...
        except Exception as e:
            notify(f"Error: {e}")

    listener = start_listener(on_scan_triggered)
    hotkey_thread = threading.Thread(target=listener.start, daemon=True)
    hotkey_thread.start()

    tray = create_tray(on_scan_triggered)
    tray.run()

if __name__ == "__main__":
    main()
```

---

## Threading Rules

- The system tray (`tray.run()`) **must** run on the main thread
- The hotkey listener **must** run in a daemon thread
- The scan function runs on the hotkey thread — this is fine since it completes in <500ms
- Do NOT use `asyncio` — use `threading` only

---

## Cross-Platform Rules

- Use `pathlib.Path` for ALL file paths — never use string concatenation or hardcoded separators
- Never use `os.path.join` — use `pathlib` instead
- Never use platform checks (`if sys.platform == 'win32'`) — the libraries handle this
- The hotkey format must use pynput syntax: `<ctrl>+<f9>` not `ctrl+f9`

---

## Error Handling Rules

- Every public function must be wrapped in try/except
- Errors must never crash the app silently — always notify the user via `notify()`
- Errors must never crash the app entirely — catch at the top level in `on_scan_triggered()`
- The only acceptable crash is on startup if a required library is missing

---

## Icon Generation

Since no icon file exists yet, generate a simple placeholder `icon.png` programmatically using Pillow at startup if the file does not exist:

```python
# Add this to main.py or a separate icon.py
from PIL import Image, ImageDraw
from pathlib import Path

def generate_placeholder_icon():
    icon_path = Path(__file__).parent / "icon.png"
    if not icon_path.exists():
        img = Image.new("RGB", (64, 64), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 54, 54], outline=(255, 255, 255), width=3)
        draw.rectangle([18, 18, 30, 30], fill=(255, 255, 255))
        draw.rectangle([34, 18, 46, 30], fill=(255, 255, 255))
        draw.rectangle([18, 34, 30, 46], fill=(255, 255, 255))
        img.save(icon_path)
```

Call `generate_placeholder_icon()` at the very start of `main()` before anything else.

---

## requirements.txt

Generate this exact file:

```
mss
pyzbar
Pillow
pynput
pystray
plyer
```

---

## README.md

Generate a brief user-facing README with:

- App name and one-line description (use the description below)
- Installation instructions for Windows, macOS, and Linux
- Usage instructions
- Hotkey default and how to change it in config.json

**App description to use:**
> SnapScan is a free, lightweight app that, when summoned, takes a screenshot, scans it for a QR code, and takes you to the target website. It's a bit like Google Lens but for PCs. SnapScan runs entirely locally — no data ever leaves your computer.

---

## What to Deliver

Deliver every file listed in the project structure, fully implemented and ready to run. Do not deliver pseudocode or placeholder logic — every function must be complete and working.

After delivering the code, provide:
1. A list of any assumptions you made
2. A list of anything that may behave differently per platform
3. Instructions for how to run the app for the first time
