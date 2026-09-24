from datetime import datetime
import platform


def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p")


def get_date():
    now = datetime.now()
    return now.strftime("%d %B %Y")


def get_system_info():
    return {
        "operating_system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }


def get_battery():
    try:
        import psutil

        battery = psutil.sensors_battery()

        if battery is None:
            return "Battery information is not available."

        return round(battery.percent)

    except Exception:
        return "Unable to retrieve battery information."
    