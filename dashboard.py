

import os
from datetime import datetime
from scheduler import Scheduler

def build_dashboard_context(scheduler):
    """Assembles the Tier 1 Dynamic Dashboard context string."""
    
    # 1. Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Get scheduled tasks
    tasks_summary = scheduler.get_dashboard_summary()
    
    # 3. Get list of notes
    notes_list = os.listdir("notes")
    notes_str = "\n".join([f"- {note}" for note in notes_list]) if notes_list else "No notes found."

    dashboard = f"""--- DYNAMIC DASHBOARD ---
    Current Time: {current_time}

    Scheduled Agent Jobs:
    {tasks_summary}

    Active Notes:
    {notes_str}
    --- END DASHBOARD ---"""
    
    return dashboard

