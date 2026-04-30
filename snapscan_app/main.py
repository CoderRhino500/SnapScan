import threading
import webbrowser
import subprocess
import sys
import os
import tempfile
import platform
from pathlib import Path
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox

# Import your new library!
from snapscan_core import Scanner

from config import load_config
from notifier import notify
from hotkey import start_listener
from tray import create_tray
from settings import show_settings 

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

def main():
    generate_placeholder_icon()
    config = load_config()
    
    # Initialize the library scanner
    scanner = Scanner()
    
    is_scanning = False 
    current_listener = None  

    def perform_scan():
        nonlocal is_scanning
        try:
            python_executable = sys.executable
            overlay_script = Path(__file__).parent / "overlay.py"
            
            result = subprocess.run(
                [python_executable, str(overlay_script)], 
                capture_output=True, 
                text=True
            )
            
            output = result.stdout.strip()
            
            if not output:
                return 
                
            x, y, w, h = map(int, output.split(','))
            
            if w <= 5 or h <= 5:
                return
                
            padding = 20
            safe_x = max(0, x - padding)
            safe_y = max(0, y - padding)
            safe_w = w + (padding * 2)
            safe_h = h + (padding * 2)
                
            # Use the library to handle capture and decode in one step
            scan_result = scanner.scan(region=(safe_x, safe_y, safe_w, safe_h))

            # Rely entirely on the ScanResult object's properties
            if scan_result.found:
                
                # Check for URLs using the library's property
                if scan_result.is_url:
                    data = scan_result.data
                    url_to_open = data if data.startswith(("http://", "https://")) else f"https://{data}"
                    
                    root = tk.Tk()
                    root.withdraw() 
                    root.attributes("-topmost", True) 

                    user_wants_to_open = messagebox.askyesno(
                        title="SnapScan - URL Detected",
                        message=f"Do you want to proceed to this link?\n\n{url_to_open}"
                    )
                    
                    root.destroy() 

                    if user_wants_to_open:
                        webbrowser.open(url_to_open)
                        notify(f"Opening: {url_to_open}")
                    else:
                        notify("Scan cancelled by user.")

                # Check for plain text using the library's property
                elif scan_result.is_text:
                    data = scan_result.data
                    root = tk.Tk()
                    root.withdraw() 
                    root.attributes("-topmost", True) 

                    preview = (data[:50] + "...") if len(data) > 50 else data

                    user_wants_to_open = messagebox.askyesno(
                        title="SnapScan - Text Detected",
                        message=f"QR code contains plain text. Do you want to open it in your default text editor?\n\nPreview:\n{preview}"
                    )
                    
                    root.destroy() 

                    if user_wants_to_open:
                        fd, temp_path = tempfile.mkstemp(suffix=".txt", prefix="SnapScan_")
                        with os.fdopen(fd, 'w', encoding='utf-8') as f:
                            f.write(data)
                        
                        if platform.system() == 'Windows':
                            os.startfile(temp_path)
                        elif platform.system() == 'Darwin': 
                            subprocess.call(('open', temp_path))
                        else: 
                            subprocess.call(('xdg-open', temp_path))
                            
                        notify("Opening text in editor...")
                    else:
                        notify("Scan cancelled by user.")
                
                # Fallback for emails, phones, wifi, etc.
                else:
                    notify(f"QR code contains: {scan_result.data}")
            else:
                notify("No QR code detected in selected region")

        except Exception as e:
            notify(f"Error: {e}")
        finally:
            is_scanning = False

    def on_scan_triggered():
        nonlocal is_scanning
        if not is_scanning:
            is_scanning = True
            threading.Thread(target=perform_scan, daemon=True).start()

    def restart_hotkey_listener():
        nonlocal current_listener
        if current_listener is not None:
            current_listener.stop() 
            
        try:
            current_listener = start_listener(on_scan_triggered)
            threading.Thread(target=current_listener.start, daemon=True).start()
        except Exception as e:
            notify(f"Error starting hotkey: {e}")

    def open_settings_window():
        threading.Thread(target=lambda: show_settings(restart_hotkey_listener), daemon=True).start()

    try:
        restart_hotkey_listener()
        tray = create_tray(on_scan_triggered, open_settings_window)
        tray.run()
    except Exception as e:
        notify(f"Fatal Startup Error: {e}")

if __name__ == "__main__":
    main()