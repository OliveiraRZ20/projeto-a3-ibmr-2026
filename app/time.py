from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def format_local_datetime(value: datetime, timezone_name: str) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    localized = value.astimezone(ZoneInfo(timezone_name))
    return localized.strftime("%d/%m/%Y %H:%M")
