import mss

def capture(monitor_index: int = 1, region: tuple = None):
    """
    Captures the screen and returns the raw mss screenshot object.
    Raises RuntimeError on failure.
    """
    try:
        with mss.MSS() as sct:
            monitors = sct.monitors
            
            # Fallback if the user requests a monitor that doesn't exist
            if monitor_index < 0 or monitor_index >= len(monitors):
                monitor_index = 1 

            if region:
                monitor_dict = {
                    "left": region[0], 
                    "top": region[1], 
                    "width": region[2], 
                    "height": region[3]
                }
            else:
                monitor_dict = monitors[monitor_index]

            screenshot = sct.grab(monitor_dict)
            return screenshot
            
    except Exception as e:
        raise RuntimeError(f"Failed to capture screenshot: {e}")