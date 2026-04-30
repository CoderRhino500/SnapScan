from pyzbar.pyzbar import decode as pyzbar_decode
from .result import ScanResult

def decode(image) -> ScanResult:
    """
    Scans a PIL Image for QR codes and always returns a structured ScanResult.
    """
    try:
        # Convert image to grayscale for higher contrast reading
        gray_image = image.convert('L')
        
        decoded_objects = pyzbar_decode(gray_image)
        
        # If nothing is found, return the default negative result
        if not decoded_objects:
            return ScanResult(found=False)

        # The spec requires we only return the first found code
        first_obj = decoded_objects[0]
        
        try:
            data = first_obj.data.decode('utf-8')
        except UnicodeDecodeError:
            # If it's binary data we can't read, consider it "not found" 
            return ScanResult(found=False)

        rect = first_obj.rect

        return ScanResult(
            found=True,
            data=data,
            type=first_obj.type,
            position=(rect.left, rect.top, rect.width, rect.height)
        )

    except Exception:
        # The library must never crash the caller's app
        return ScanResult(found=False)