from .capture import capture
from .converter import to_pil
from .decoder import decode
from .result import ScanResult

class Scanner:
    def __init__(self, monitor: int = 1):
        self.monitor = monitor

    def scan(self, region: tuple = None) -> ScanResult:
        """
        Takes a screenshot and scans it. 
        Always returns a ScanResult. Never raises exceptions.
        """
        try:
            raw_screenshot = capture(monitor_index=self.monitor, region=region)
            pil_image = to_pil(raw_screenshot)
            return decode(pil_image)
        except Exception:
            return ScanResult(found=False)

    def scan_image(self, image) -> ScanResult:
        """
        Allows developers to pass their own PIL image directly into the scanner.
        """
        try:
            return decode(image)
        except Exception:
            return ScanResult(found=False)