import pystray
from PIL import Image
from pathlib import Path

def create_tray(scan_callback, settings_callback):
    try:
        icon_path = Path(__file__).parent / "icon.png"
        if icon_path.exists():
            image = Image.open(icon_path)
        else:
            image = Image.new("RGB", (64, 64), color=(30, 30, 30))

        def on_quit(icon, item):
            icon.stop()

        def on_scan(icon, item):
            scan_callback()
            
        def on_settings(icon, item):
            settings_callback()

        menu = pystray.Menu(
            pystray.MenuItem("SnapScan", None, enabled=False),
            pystray.MenuItem("Settings", on_settings),  # Added Settings Button
            pystray.MenuItem("Scan Now", on_scan),
            pystray.MenuItem("Quit", on_quit)
        )

        icon = pystray.Icon("SnapScan", image, "SnapScan", menu)
        return icon
    except Exception as e:
        raise Exception(f"Failed to create tray icon: {e}")