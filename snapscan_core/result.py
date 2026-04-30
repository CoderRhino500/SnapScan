from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Tuple

@dataclass
class ScanResult:
    found: bool                          
    data: Optional[str] = None           
    type: Optional[str] = None           
    position: Optional[Tuple] = None     
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
        data_preview = self.data[:50] + "..." if len(self.data) > 50 else self.data
        return f"ScanResult(found=True, type={self.type}, data={data_preview})"