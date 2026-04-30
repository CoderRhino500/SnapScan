# SnapScan — Problem Statement & Project Documentation

## Title
**SnapScan: Cross-Platform Screenshot-Based QR Scanner as Both a Desktop Application and Reusable Python Library**

---

## Problem Statement
Traditional QR scanners primarily rely on webcams or mobile devices, making it inconvenient to scan QR codes already present on a computer screen, inside documents, presentations, websites, or screenshots. Existing solutions often lack a lightweight desktop-native approach with region selection, global hotkey access, system tray integration, and reusable developer APIs.

**SnapScan** addresses this problem by providing:

1. **A Desktop Application** for end users to scan QR codes directly from any selected screen region.
2. **A Python Library (`snapscan-core`)** for developers to integrate screenshot-based QR scanning into their own applications.

This dual architecture makes SnapScan both a standalone productivity tool and a reusable software component. fileciteturn0file0 fileciteturn0file4

---

# Objective
The objective of SnapScan is to develop a lightweight, cross-platform system that:

- Captures user-selected screen regions.
- Detects and decodes QR codes from screenshots.
- Supports URL and text handling workflows.
- Offers quick access through global hotkeys and tray controls.
- Provides a reusable Python package for external developers.

---

# Scope of the Project
SnapScan covers two major components:

## 1. SnapScan Desktop Application
The desktop app includes:

### Screen Region Capture
Users select a region using a fullscreen transparent overlay with drag selection. fileciteturn0file6

### Global Hotkey Trigger
Scanning can be launched instantly using configurable shortcuts (default Ctrl+F8/F9).  fileciteturn0file1 fileciteturn0file3

### QR Detection and Action Handling
The application:
- Opens URLs in a browser after user confirmation.
- Opens plain text QR contents in the default text editor.
- Detects special formats like:
  - URLs
  - Email QR codes
  - Phone QR codes
  - Wi-Fi QR codes

Powered by structured `ScanResult` properties.  fileciteturn0file13

### System Tray Integration
Provides:
- Scan Now
- Settings
- Quit

via tray menu. fileciteturn0file8

### Configurable Settings
Supports:
- Hotkey customization
- Notification duration
- Auto-open options
- Monitor selection

fileciteturn0file2 fileciteturn0file7

---

## 2. SnapScan Python Library (`snapscan-core`)
Beyond the app, SnapScan has been modularized into a reusable library. This is a major project contribution.

### Library Features
The library exposes:

```python
from snapscan_core import Scanner, ScanResult
```

Supports:

### Screenshot Capture Module
```python
capture()
```
Captures full monitors or custom regions.  
fileciteturn0file10

### Image Conversion Module
```python
to_pil()
```
Converts raw MSS captures into Pillow images.

fileciteturn0file11

### QR Decoder Module
```python
decode()
```
Uses `pyzbar` to decode QR codes.

fileciteturn0file12

### Scanner Class
```python
scanner = Scanner()
result = scanner.scan(region=(x,y,w,h))
```

Also supports:
```python
scanner.scan_image(image)
```

fileciteturn0file14

### Structured ScanResult Model
Encapsulates:
- Found status
- Decoded data
- Type
- Position
- Timestamp
- Data classification helpers

fileciteturn0file13

### Package Distribution
Packaged via:
```python
setup.py
```
with dependencies:
- mss
- pyzbar
- Pillow

fileciteturn0file0

---

# Technology Stack
## Frontend/UI
- Tkinter (overlay and dialogs)
- PyStray (system tray)
- Plyer (notifications)

## Backend
- Python
- MSS
- Pillow
- PyZbar
- Pynput

---

# System Architecture
## Application Flow
1. User presses global hotkey.
2. Overlay opens for region selection.
3. Screenshot captured.
4. Library processes image.
5. QR decoded.
6. Result handled (URL/text/etc.)
7. Notification displayed.

Main app orchestrates library usage through:

```python
scan_result = scanner.scan(region=(safe_x,safe_y,safe_w,safe_h))
```

fileciteturn0file4

---

# Key Features
## User Features
- Screenshot-based QR scanning
- No webcam required
- Global shortcut access
- Tray controls
- Interactive confirmation dialogs
- Text extraction from QR

## Developer Features
- Importable Python package
- Structured APIs
- Fail-safe ScanResult returns
- Modular architecture
- Cross-platform support

---

# Innovation / Novelty
The novelty of SnapScan lies in combining:

## End-User Desktop Product
A ready-to-use QR scanning utility.

AND

## Reusable Developer Library
A package developers can integrate into their own projects.

Most projects stop at one of these; SnapScan provides both.

---

# Modules Used
| Module | Purpose |
|-------|---------|
| main.py | Main application orchestration |
| overlay.py | Screen region selector |
| hotkey.py | Global shortcut handling |
| tray.py | System tray controls |
| settings.py | User configuration UI |
| notifier.py | Notifications |
| capture.py | Screenshot capture |
| converter.py | MSS to PIL conversion |
| decoder.py | QR decoding |
| result.py | Structured scan results |
| scanner.py | Core scanner engine |

---

# Expected Outcome
The project produces:

- A functional desktop QR scanner.
- A distributable Python package.
- Faster QR scanning from on-screen content.
- Reusable scanning infrastructure for other developers.

---

# Future Enhancements
Possible extensions:

- Multi-QR detection
- QR scan history
- OCR support
- Barcode support
- Linux/Mac packaging installers
- GUI theme improvements
- Plugin support for library extensions

---

# Conclusion
SnapScan solves the problem of scanning QR codes directly from screen content by combining a desktop application with a reusable Python library. The desktop app offers usability through hotkeys, overlays, notifications and tray controls, while `snapscan-core` makes the same functionality available for developer integration.

This dual app-plus-library architecture is a distinguishing strength of the project. 

