# SnapScan - Comprehensive Hackathon Guide

## 🚀 1. Elevator Pitch (The "Hook" for Judges)
**What is SnapScan?** SnapScan is a lightweight, cross-platform, privacy-first desktop application that brings the power of "Google Lens" to your PC. Running silently in the background, users can press a global hotkey, draw a selection box over any part of their screen, and instantly decode QR codes. 

**The core philosophy:** * **Zero Cloud:** All image processing and decoding happen locally in memory. No screenshots are saved to disk, and no data is sent to external APIs.
* **Frictionless UI:** No clunky main window. It lives in the system tray and uses minimal resources, making it accessible even on low-end machines (2GB RAM).

---

## ✨ 2. Key Features (Slide Deck Highlights)

* **Precision Screen Sniping:** A native, DPI-aware screen-dimming overlay allows users to select exact regions, preventing mis-scans on cluttered screens.
* **Smart Content Handling:** * Automatically detects URLs and safely asks for user confirmation before launching the default browser.
  * Captures plain text, previews it, and seamlessly opens it in the system's default text editor via secure temporary files.
* **Dynamic Customization:** Features a native Settings UI allowing users to remap their global hotkeys on the fly, instantly restarting background listeners without needing an app reboot.
* **Cross-Platform:** Built to work uniformly across Windows, macOS, and Linux.

---

## 🏗️ 3. Architecture & File Structure (Technical Details Slide)

The application is modularized into **12 precise files** ensuring clean code and separation of concerns.

### The Core Engine
* **`main.py` (The Orchestrator):** The entry point. It manages complex multi-threading to ensure the system tray, keyboard listeners, and Tkinter GUI popups do not block each other. It also houses the smart URL validation and file-handling logic.
* **`overlay.py` (The Snipping Tool):** A standalone Tkinter script that creates a borderless, transparent screen overlay. It captures mouse drag events to define the target area.
* **`scanner.py`:** Uses `pyzbar` to decode the image. It converts incoming images to grayscale first to maximize contrast and reliability.
* **`screenshot.py`:** Utilizes the fast `mss` library to grab the exact pixel region defined by the overlay, feeding it directly into a Pillow image buffer in memory.

### Background Services & UI
* **`hotkey.py`:** Leverages `pynput` to listen for the user's global hotkey across the entire OS.
* **`tray.py`:** Uses `pystray` to maintain the persistent, right-clickable system tray icon (with dynamically generated placeholder graphics via `icon.png` if missing).
* **`settings.py`:** Provides a native `tkinter` popup for users to view and update their hotkey. It safely signals `main.py` to kill and reload the background listener when settings change.
* **`notifier.py`:** Interfaces with OS-native toast notifications (`plyer`) to provide non-intrusive status updates.

### Configuration & Dependencies
* **`config.py` & `config.json`:** Manages persistent user preferences using Python's cross-platform `pathlib`.
* **`requirements.txt`:** Lists the lightweight stack: `mss`, `pyzbar`, `Pillow`, `pynput`, `pystray`, `plyer`.

---

## 🚧 4. Technical Challenges Overcome (The "Flex" Slide)
Judges love knowing what problems you solved. Highlight these in the presentation:

1. **The "Blocked Thread" Deadlock:** * *Problem:* Launching the GUI overlay blocked the hotkey listener, preventing it from registering the "key release" event, causing a memory loop.
   * *Solution:* Decoupled the scanning logic into separate worker threads (`threading.Thread(target=perform_scan, daemon=True)`), allowing the listener to instantly reset.
2. **Windows DPI Scaling Bugs:** * *Problem:* Display scaling (e.g., 125%) caused the drawn overlay coordinates to misalign with physical screen pixels, resulting in screenshots of empty space.
   * *Solution:* Injected Windows C-library bindings (`ctypes.windll.shcore.SetProcessDpiAwareness`) to force 1:1 pixel mapping.
3. **The QR "Quiet Zone" Failure:** * *Problem:* Users draw boxes too tightly around QR codes, cutting off the required white border, causing scan failures.
   * *Solution:* Programmed `main.py` to automatically inject a 20-pixel invisible padding buffer around the user's selection to guarantee a successful read.
4. **Cross-Platform File Launching:** * *Problem:* Plain-text QR codes couldn't be easily passed to native editors from background tasks.
   * *Solution:* Used Python's `tempfile` to securely write the data, paired with OS-specific commands (`os.startfile` for Windows, `open` for Mac, `xdg-open` for Linux) to seamlessly trigger default apps.

---

## 🔮 5. Future Scope
* OCR implementation to read standard text from screenshots.
* Localized history logging to review past scanned links safely.
* Wayland compatibility optimizations for modern Linux distros.
