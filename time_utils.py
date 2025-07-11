
import dateparser

def parse_schedule(schedule_str: str) -> str:
    """Parses a human-readable schedule string and returns a cron expression."""
    # First, handle recurring schedules which dateparser doesn't directly support for cron conversion.
    if "every hour" in schedule_str.lower():
        return "0 * * * *"
    if "every day at" in schedule_str.lower():
        time_str = schedule_str.lower().split("at")[1].strip()
        try:
            # Use dateparser to handle time formats like "5pm" or "17:00"
            parsed_time = dateparser.parse(time_str)
            return f"{parsed_time.minute} {parsed_time.hour} * * *"
        except:
            return None # Could not parse the time part
    if "every weekday at" in schedule_str.lower():
        time_str = schedule_str.lower().split("at")[1].strip()
        try:
            parsed_time = dateparser.parse(time_str)
            return f"{parsed_time.minute} {parsed_time.hour} * * 1-5"
        except:
            return None

    # Handle one-time schedules using dateparser
    dt = dateparser.parse(schedule_str)
    
    if dt:
        # Ensure the parsed date is in the future
        from datetime import datetime
        if dt < datetime.now():
             # If you want to handle this case, you might add logic here.
             # For now, we assume the user wants a future event.
             pass
        return f"{dt.minute} {dt.hour} {dt.day} {dt.month} *"
    
    return None
