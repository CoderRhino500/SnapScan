import tkinter as tk
import sys
import platform

# CRITICAL FIX: Tell Windows to use actual physical pixels, ignoring 125%/150% scaling
if platform.system() == "Windows":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2) # Per monitor DPI aware
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware() # Fallback for older Windows
        except Exception:
            pass

class ScreenOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.config(cursor="crosshair")
        
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.start_x = 0
        self.start_y = 0
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, 
            outline="red", width=2
        )

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        
        width = x2 - x1
        height = y2 - y1
        
        print(f"{x1},{y1},{width},{height}")
        sys.stdout.flush()
        
        self.root.destroy()

if __name__ == "__main__":
    app = ScreenOverlay()
    app.root.mainloop()