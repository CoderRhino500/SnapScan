import tkinter as tk
from tkinter import messagebox
from config import load_config, save_config

def show_settings(on_save_callback):
    config = load_config()
    
    root = tk.Tk()
    root.title("SnapScan Settings")
    root.geometry("350x180")
    root.attributes("-topmost", True) # Keep it above other windows
    root.resizable(False, False)

    tk.Label(root, text="Global Hotkey:", font=("Arial", 10, "bold")).pack(pady=(15, 5))
    
    # Load the current hotkey from config
    hotkey_var = tk.StringVar(value=config.get("hotkey", "<ctrl>+<f9>"))
    entry = tk.Entry(root, textvariable=hotkey_var, font=("Arial", 12), width=20, justify="center")
    entry.pack(pady=5)
    
    # Helpful format instructions for the user
    tk.Label(root, text="Format: <ctrl>+<shift>+s or <alt>+<f9>", font=("Arial", 8), fg="gray").pack()

    def save_and_close():
        new_hotkey = hotkey_var.get().strip().lower()
        if not new_hotkey:
            messagebox.showerror("Error", "Hotkey cannot be empty.")
            return
        
        # Save to config.json
        config["hotkey"] = new_hotkey
        save_config(config)
        
        # Tell main.py to reload the keyboard listener
        if on_save_callback:
            on_save_callback()
            
        messagebox.showinfo("Success", f"Hotkey successfully updated to {new_hotkey}!")
        root.destroy()

    tk.Button(root, text="Save Settings", command=save_and_close, width=15).pack(pady=15)
    
    root.mainloop()