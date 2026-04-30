# SnapScan 📷

> A free, lightweight desktop app that scans QR codes from your screen and opens them instantly — like Google Lens, but for PCs.

SnapScan sits silently in your system tray. Press a hotkey, and it captures your screen, detects any QR code, and opens the URL in your browser — all in under a second. No sign-in. No internet required. No data ever leaves your computer.

---

## ✨ Features

- 🔍 **One hotkey, instant scan** — press `Ctrl+F9` (Or whatever Hotkey you have assigned) and SnapScan does the rest
- 🖥️ **Lives in your system tray** — no window, no clutter, always ready
- 🔒 **100% local** — nothing is sent to any server, ever
- 🪶 **Lightweight** — runs comfortably on machines with as little as 2GB RAM
- 🌍 **Cross-platform** — Windows, macOS, and Linux
- 🔓 **No login required** — download and run, that's it
- 📖 **Open source** — free forever

---

## 📸 How It Works

1. A QR code appears somewhere on your screen
2. Press `Ctrl+F9`(Or whatever Hotkey you have assigned)
3. SnapScan captures the screen, finds the QR code, and opens the URL in your browser
4. A notification confirms what was found

That's it.

---

## 🚀 Installation

### Prerequisites

**All platforms:**
```bash
pip install mss pyzbar pynput pystray plyer Pillow
```

**macOS only** — install zbar via Homebrew:
```bash
brew install zbar
```

**Linux (Debian/Ubuntu) only:**
```bash
sudo apt install libzbar0
```

**Linux (Fedora/RHEL) only:**
```bash
sudo dnf install zbar
```

**Windows** — no extra steps needed beyond pip.

---

### Run from Source

```bash
# 1. Clone the repo
git clone https://github.com/CoderRhino500/SnapScan.git
cd SnapScan

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python main.py
```

SnapScan will appear in your system tray and is immediately ready to use.

---

### Download a Pre-built Binary

Pre-built executables for Windows, macOS, and Linux are available on the [Releases](https://github.com/CoderRhino500/SnapScan/releases) page.

| Platform | Download |
|---|---|
| Windows | `SnapScan.exe` |
| macOS | `SnapScan.app` |
| Linux | `SnapScan` |

> **Coming soon** — binaries will be available with the first stable release.

---

## 🖱️ Usage

| Action | How |
|---|---|
| Scan a QR code | Press `Ctrl+F9` |
| Scan manually | Right-click tray icon → "Scan Now" |
| Quit the app | Right-click tray icon → "Quit" |
| Change hotkey | Edit `config.json` |

---

## ⚙️ Configuration

SnapScan reads its settings from `config.json` in the app directory. Edit this file to customise the app:

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

| Setting | Default | Description |
|---|---|---|
| `hotkey` | `<ctrl>+<f9>` | Global hotkey to trigger a scan |
| `notification_duration` | `3` | How long toast notifications stay on screen (seconds) |
| `auto_open_urls` | `true` | Automatically open URLs in browser when found |
| `monitor` | `1` | Which monitor to scan (1 = primary) |
| `save_history` | `false` | Save scan history locally |
| `url_validation` | `true` | Only open links that start with http/https/www |

### Hotkey Format

Hotkeys follow pynput syntax. Some examples:

| Hotkey | config.json value |
|---|---|
| Ctrl + F9 | `<ctrl>+<f9>` |
| Ctrl + Shift + S | `<ctrl>+<shift>+s` |
| Alt + Q | `<alt>+q` |

---

## 🗂️ Project Structure

```
SnapScan/
│
├── snapscan_app/
│   ├── main.py          # Entry point
│   ├── hotkey.py        # Global hotkey listener
│   ├── tray.py          # System tray icon and menu
│   ├── notifier.py      # Toast notifications
│   └── config.py        # Configuration loader
│
├── snapscan_core/       # Core library (see snapscan-core below)
│   ├── __init__.py
│   ├── scanner.py
│   ├── capture.py
│   ├── decoder.py
│   ├── converter.py
│   └── result.py
│
├── config.json          # User configuration
├── requirements.txt     # pip dependencies
├── icon.png             # Tray icon
├── LICENSE
└── README.md
```

---

## 📦 snapscan-core

The scanning engine that powers SnapScan is also available as a standalone Python library called **snapscan-core**. It lets any developer add QR code screenshot scanning to their own Python apps in three lines of code:

```python
from snapscan_core import Scanner

result = Scanner().scan()
if result.is_url:
    print(result.data)
```

> **pip install snapscan-core** — coming soon to PyPI

See the [snapscan-core documentation](https://github.com/CoderRhino500/SnapScan/blob/main/SnapScan-core%20(Library).md) for full details.

---

## 🧩 Platform Notes

| Platform | Status | Notes |
|---|---|---|
| Windows | ✅ Supported | No extra dependencies |
| macOS | ✅ Supported | Requires `brew install zbar` |
| Linux X11 | ✅ Supported | Requires `libzbar0` |
| Linux Wayland | ⚠️ Limited | Run in X11 mode for best results |

### macOS Permissions

On first run, macOS will ask for two permissions:
- **Accessibility** — required for the global hotkey to work
- **Screen Recording** — required to capture the screen

Both prompts will appear automatically. SnapScan does not record or store your screen at any time.

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `mss` | Fast cross-platform screenshot capture |
| `pyzbar` | QR code decoding |
| `Pillow` | Image format conversion |
| `pynput` | Global hotkey listener |
| `pystray` | System tray icon |
| `plyer` | Cross-platform toast notifications |
| `webbrowser` | Open URLs in default browser |

---

## 🗺️ Roadmap

### v1.0 — Stable Release
- [x] Project planning and architecture
- [ ] Core screenshot + QR decode flow
- [ ] Global hotkey support
- [ ] System tray integration
- [ ] Toast notifications
- [ ] Cross-platform testing
- [ ] Pre-built binaries (Windows, macOS, Linux)

### v2.0 — Library Release
- [ ] snapscan-core published to PyPI
- [ ] Region selection (drag to select area)
- [ ] Multiple QR code detection
- [ ] Scan history

### Future Ideas
- Barcode support beyond QR (EAN-13, Code 128, etc.)
- OCR — read text from screen selection
- CLI mode for scripting and automation
- Auto-update support

---

## 🤝 Contributing

Contributions are welcome! If you find a bug, have a feature request, or want to submit a pull request:

1. [Open an issue](https://github.com/CoderRhino500/SnapScan/issues)
2. Fork the repo
3. Create a branch (`git checkout -b feature/your-feature`)
4. Commit your changes (`git commit -m 'Add your feature'`)
5. Push to your branch (`git push origin feature/your-feature`)
6. Open a Pull Request

Please keep contributions lightweight and in the spirit of the project — fast, local, and privacy-respecting.

---

## 📜 License

- **SnapScan app** — [GPL v3](LICENSE)
- **snapscan-core library** — LGPL v3

SnapScan is and always will be free and open source.

---

## 🙏 Acknowledgements

Built with the help of these excellent open source libraries:
- [mss](https://github.com/BoboTiG/python-mss)
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)
- [pynput](https://github.com/moses-palmer/pynput)
- [pystray](https://github.com/moses-palmer/pystray)
- [plyer](https://github.com/kivy/plyer)
- [Pillow](https://github.com/python-pillow/Pillow)

---

<p align="center">
  Made with ❤️ by Manuhe Manuhor Baabe — Scan smarter, not harder.
</p>
