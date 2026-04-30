from plyer import notification
from config import load_config

def notify(message):
    try:
        config = load_config()
        duration = config.get("notification_duration", 3)
        notification.notify(
            title="SnapScan",
            message=str(message),
            app_name="SnapScan",
            timeout=duration
        )
    except Exception:
        pass