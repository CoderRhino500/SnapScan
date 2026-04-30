# SnapScan-core (Library)

## Overview

This document is a complete specification for converting the SnapScan standalone app into a reusable Python library called `snapscan-core`. It is written to be understood and implemented by both human developers and AI coding assistants. Follow every instruction exactly.

---

## What snapscan-core Is

`snapscan-core` is the extracted, reusable brain of the SnapScan application. It handles one job and one job only:

> **"Take a screenshot, scan it for a QR code, and return a structured result."**

It does not handle hotkeys, system trays, browser opening, notifications, or config files. Those remain in the SnapScan app. The library is completely passive — it does nothing until explicitly called by external code.

---

## What snapscan-core Is NOT

- It is NOT a standalone app
- It does NOT listen for hotkeys
- It does NOT open browsers
- It does NOT show notifications
- It does NOT manage a config file
- It does NOT make any network requests
- It does NOT save screenshots to disk
- It does NOT decide what happens after a scan — that is the caller's responsibility

---

## Repository Structure

Use a monorepo approach. Both the library and the app live in the same GitHub repository during development. Split into separate repos only when the library is stable and ready for PyPI.

```
SnapScan/
│
├── snapscan_core/           # The library (reusable, publishable)
│   ├── __init__.py          # Public API exports
│   ├── capture.py           # Screenshot capture logic
│   ├── converter.py         # Image format conversion logic
│   ├── decoder.py           # QR code decoding logic
│   ├── result.py            # ScanResult data class
│   └── scanner.py           # Main Scanner class (entry point for callers)
│
├── snapscan_app/            # The app (uses the library)
│   ├── main.py              # Entry point
│   ├── hotkey.py            # Global hotkey listener
│   ├── tray.py              # System tray icon and menu
│   ├── notifier.py          # Toast notifications
│   └── config.py            # App configuration
│
├── tests/                   # Tests for the library
│   ├── test_capture.py
│   ├── test_decoder.py
│   ├── test_result.py
│   └── test_scanner.py
│
├── examples/                # Example scripts showing library usage
│   ├── basic_scan.py
│   ├── cli_tool.py
│   └── timer_scan.py
│
├── setup.py                 # Library packaging configuration
├── requirements.txt         # App dependencies
├── requirements-core.txt    # Library-only dependencies
├── LICENSE                  # LGPL v3 for the library
└── README.md
```

---

## Development Order

Do NOT build the library and app simultaneously from scratch. Follow this exact order:

1. Build the SnapScan app first as a single working codebase
2. Confirm the app works correctly on all platforms
3. Identify the natural seams between reusable logic and app-specific logic
4. Extract the library by moving screenshot, conversion, and decoding logic into `snapscan_core/`
5. Refactor the SnapScan app to import from `snapscan_core` instead of its own modules
6. Write tests for the library
7. Write example scripts
8. Publish to PyPI when stable

---

## Library Dependencies

The library must only depend on what is strictly necessary for screenshot capture and QR decoding. It must NOT depend on any app-specific libraries.

### requirements-core.txt
```
mss
pyzbar
Pillow
```

That is all. No pynput, no pystray, no plyer. Those are app dependencies only.

### System Dependencies (documented for users)

**macOS:**
```bash
brew install zbar
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install libzbar0
```

**Windows:** No extra dependencies needed.

---

## File-by-File Specification

### result.py — The ScanResult Class

This is the most important design decision in the library. Every scan returns a `ScanResult` object — never a raw dict, never None. The caller always gets a predictable, structured object.

```python
# result.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Tuple

@dataclass
class ScanResult:
    found: bool                          # True if a QR code was detected
    data: Optional[str] = None           # Raw decoded string content
    type: Optional[str] = None           # Barcode type e.g. 'QRCODE', 'EAN13'
    position: Optional[Tuple] = None     # (x, y, width, height) on screen
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def is_url(self) -> bool:
        if not self.data:
            return False
        return self.data.startswith(('http://', 'https://', 'www.'))

    @property
    def is_email(self) -> bool:
        if not self.data:
            return False
        return self.data.startswith('mailto:')

    @property
    def is_phone(self) -> bool:
        if not self.data:
            return False
        return self.data.startswith('tel:')

    @property
    def is_wifi(self) -> bool:
        if not self.data:
            return False
        return self.data.startswith('WIFI:')

    @property
    def is_text(self) -> bool:
        return (
            self.found and
            not self.is_url and
            not self.is_email and
            not self.is_phone and
            not self.is_wifi
        )

    def __repr__(self):
        if not self.found:
            return "ScanResult(found=False)"
        return f"ScanResult(found=True, type={self.type}, data={self.data[:50]}...)"
```

**Rules:**
- `ScanResult` must always be returned — even when nothing is found (`found=False`)
- Never return `None` from any public function
- All properties must be safe to call regardless of whether `found` is True or False

---

### capture.py — Screenshot Capture

```python
# capture.py — Expected interface and behaviour

# Expose one public function: capture(monitor)
# monitor: integer index of monitor to capture (default: 1 = primary)
# Returns: a PIL Image object
# Raises: RuntimeError if capture fails (never returns None)
# Never saves the screenshot to disk
# Never keeps the screenshot in memory after returning
```

**Implementation rules:**
- Use `mss` for capturing
- Convert BGRA output from mss to RGB PIL Image using `Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")`
- Default monitor index is `1` (primary monitor)
- Accept `monitor` as a parameter so callers can specify which screen to capture
- Wrap in try/except and raise a descriptive `RuntimeError` on failure

**Expected usage:**
```python
from snapscan_core.capture import capture

image = capture()           # Primary monitor
image = capture(monitor=2)  # Second monitor
```

---

### converter.py — Image Format Conversion

```python
# converter.py — Expected interface and behaviour

# Expose one public function: to_pil(screenshot)
# screenshot: raw mss screenshot object
# Returns: PIL Image in RGB format
# This module exists to isolate the conversion logic
# so it can be changed independently of capture logic
```

**Implementation rules:**
- Keep this module simple — one function, one job
- Use the exact conversion: `Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")`
- Do NOT add any image processing, filtering, or enhancement here

---

### decoder.py — QR Code Decoding

```python
# decoder.py — Expected interface and behaviour

# Expose one public function: decode(image)
# image: PIL Image object
# Returns: ScanResult object (always — never None)
# If multiple QR codes found, return only the first one
# Handle UnicodeDecodeError gracefully
```

**Implementation rules:**
- Use `pyzbar.pyzbar.decode()` to scan the image
- If `detected` list is empty, return `ScanResult(found=False)`
- If detected, take `detected[0]` (first result only)
- Decode bytes to string using `utf-8`
- Catch `UnicodeDecodeError` — if binary data, return `ScanResult(found=False)`
- Populate `position` from `detected[0].rect` as a tuple `(left, top, width, height)`
- Populate `type` from `detected[0].type`

**Expected usage:**
```python
from snapscan_core.decoder import decode

result = decode(image)
print(result.found)   # True or False
print(result.data)    # 'https://example.com' or None
```

---

### scanner.py — Main Entry Point

This is the only file callers need to import from. It ties capture and decode together into one clean interface.

```python
# scanner.py — Expected interface and behaviour

class Scanner:
    def __init__(self, monitor: int = 1):
        # monitor: which screen to capture (default 1 = primary)
        self.monitor = monitor

    def scan(self) -> ScanResult:
        # 1. Capture screenshot using capture.py
        # 2. Decode using decoder.py
        # 3. Return ScanResult
        # Never raises — catches all exceptions and returns ScanResult(found=False)
        pass

    def scan_image(self, image) -> ScanResult:
        # Accept an existing PIL Image instead of taking a screenshot
        # Useful for developers who already have an image
        # Decode and return ScanResult
        pass
```

**Rules:**
- `scan()` must never raise an exception — catch everything, return `ScanResult(found=False)` on any error
- `scan_image()` allows passing in an existing image — this makes the library more flexible
- Both methods always return a `ScanResult` object

**Expected usage:**
```python
from snapscan_core import Scanner

# Basic usage
scanner = Scanner()
result = scanner.scan()

# Specific monitor
scanner = Scanner(monitor=2)
result = scanner.scan()

# Scan an existing image
from PIL import Image
img = Image.open("test.png")
result = scanner.scan_image(img)
```

---

### __init__.py — Public API

This file defines exactly what developers see when they import `snapscan_core`. Keep it clean and minimal.

```python
# __init__.py

from snapscan_core.scanner import Scanner
from snapscan_core.result import ScanResult

__version__ = "0.1.0"
__all__ = ["Scanner", "ScanResult"]
```

**Rules:**
- Only export `Scanner` and `ScanResult` — these are the entire public API
- Internal modules (`capture`, `converter`, `decoder`) are implementation details
- Developers should never need to import from internal modules directly

---

## How the SnapScan App Uses the Library

After extraction, the app's `main.py` scan flow changes from calling its own internal modules to calling the library:

### Before (app calling its own modules):
```python
from screenshot import capture
from scanner import scan

image = capture()
result = scan(image)
```

### After (app calling the library):
```python
from snapscan_core import Scanner

scanner = Scanner()
result = scanner.scan()
```

Everything else in the app (hotkey, tray, notifier, config) stays exactly the same. Only the scan call changes.

---

## The ScanResult in the App

The app then acts on the result exactly as before, using the new ScanResult properties:

```python
def on_scan_triggered():
    result = scanner.scan()

    if result.found:
        if result.is_url:
            webbrowser.open(result.data)
            notify(f"Opening: {result.data}")
        elif result.is_email:
            webbrowser.open(result.data)
            notify(f"Opening email: {result.data}")
        elif result.is_wifi:
            notify(f"WiFi credentials found: {result.data}")
        else:
            notify(f"QR contains: {result.data}")
    else:
        notify("No QR code detected")
```

---

## setup.py — Library Packaging

When ready to publish to PyPI, use this configuration:

```python
from setuptools import setup, find_packages

setup(
    name="snapscan-core",
    version="0.1.0",
    description="Lightweight cross-platform screenshot QR code scanner library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    url="https://github.com/yourusername/SnapScan",
    packages=find_packages(include=["snapscan_core"]),
    install_requires=[
        "mss",
        "pyzbar",
        "Pillow",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
    ],
)
```

**To publish:**
```bash
pip install build twine
python -m build
twine upload dist/*
```

**Developers install with:**
```bash
pip install snapscan-core
```

---

## License

- `snapscan_core/` — **LGPL v3**
  - The library itself must stay open source
  - Apps that import and use the library do NOT have to be open source
  - This maximises developer adoption

- `snapscan_app/` — **GPL v3**
  - The app itself must always stay open source
  - Any derivatives of the app must also be GPL v3

---

## Tests

Write tests for every public function in the library. Place all tests in the `tests/` directory.

### Minimum required tests:

**test_result.py**
- Test `ScanResult(found=False)` returns correct defaults
- Test `is_url` returns True for http/https/www URLs
- Test `is_email` returns True for mailto: links
- Test `is_phone` returns True for tel: links
- Test `is_wifi` returns True for WIFI: strings
- Test `is_text` returns True for plain text
- Test `__repr__` returns readable string

**test_decoder.py**
- Test decoding a known QR code image returns correct data
- Test decoding a blank image returns `ScanResult(found=False)`
- Test decoding an image with multiple QR codes returns only the first

**test_scanner.py**
- Test `Scanner()` initialises with default monitor=1
- Test `Scanner(monitor=2)` sets monitor correctly
- Test `scan_image()` with a known QR code image returns correct result
- Test `scan_image()` with a blank image returns `ScanResult(found=False)`

---

## Example Scripts

Include these in the `examples/` directory to show developers how to use the library:

### examples/basic_scan.py
```python
# Most basic usage — scan and print result
from snapscan_core import Scanner

scanner = Scanner()
result = scanner.scan()

if result.found:
    print(f"Found: {result.data}")
    print(f"Type: {result.type}")
else:
    print("No QR code found")
```

### examples/cli_tool.py
```python
# Command line QR scanner using snapscan-core
import sys
import webbrowser
from snapscan_core import Scanner

scanner = Scanner()
result = scanner.scan()

if result.found:
    print(f"QR Code detected: {result.data}")
    if result.is_url:
        webbrowser.open(result.data)
        print("Opening in browser...")
    sys.exit(0)
else:
    print("No QR code detected")
    sys.exit(1)
```

### examples/timer_scan.py
```python
# Continuously scan every 2 seconds — useful for kiosk apps
import time
from snapscan_core import Scanner

scanner = Scanner()

print("Scanning continuously. Press Ctrl+C to stop.")
while True:
    result = scanner.scan()
    if result.found:
        print(f"[{result.timestamp}] Found: {result.data}")
    time.sleep(2)
```

---

## Version Roadmap

### v0.1.0 — Initial Release
- `Scanner` class with `scan()` and `scan_image()`
- `ScanResult` with all properties
- Full platform support (Windows, macOS, Linux)
- Published to PyPI

### v0.2.0 — Planned
- Region selection support — pass a bounding box to scan a specific area
- Multi-QR support — return all detected codes, not just the first
- Optional image preprocessing for better detection accuracy

### v1.0.0 — Stable API
- API frozen — no breaking changes after this point
- Full test coverage
- Complete documentation site
