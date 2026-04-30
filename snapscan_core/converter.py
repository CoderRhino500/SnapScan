from PIL import Image

def to_pil(screenshot):
    """
    Converts a raw mss screenshot object into a standard RGB Pillow Image.
    """
    try:
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img
    except Exception as e:
        raise RuntimeError(f"Failed to convert screenshot to PIL Image: {e}")