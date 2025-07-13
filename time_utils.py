
from croniter import croniter
from datetime import datetime
import re

def parse_schedule(schedule_string: str) -> str:
    """Parses a human-readable schedule string into a cron expression."""
    schedule_string = schedule_string.lower()
    now = datetime.now()

    # Handle cron expressions directly
    try:
        croniter(schedule_string, now)
        return schedule_string
    except ValueError:
        pass

    # Handle natural language
    if "every day" in schedule_string or "daily" in schedule_string:
        match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', schedule_string)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if match.group(3) == "pm" and hour != 12:
                hour += 12
            return f"{minute} {hour} * * *"
        else:
            return "0 9 * * *"  # Default to 9am
    elif "every hour" in schedule_string:
        return "0 * * * *"
    elif "every minute" in schedule_string:
        return "* * * * *"
    elif "tomorrow at" in schedule_string:
        match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', schedule_string)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if match.group(3) == "pm" and hour != 12:
                hour += 12
            return f"{minute} {hour} * * *"
    
    return None
