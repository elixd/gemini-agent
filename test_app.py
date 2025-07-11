import os
import json
import time
from functions import create_note, update_note
from llm_handler import get_llm_response
from scheduler import Scheduler

def strip_markdown_fences(text):
    """Removes markdown code fences from a string."""
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

# --- Test Note Management ---
print("--- Testing Note Management ---")
NOTE_TOPIC = "house_project_test"

# 1. Create a note
print(create_note(NOTE_TOPIC))

# 2. Update the note
print(update_note(NOTE_TOPIC, "Contacted architect"))
print(update_note(NOTE_TOPIC, "Reviewed blueprints"))

# 3. Verify note content
note_path = os.path.join("notes", f"{NOTE_TOPIC}.md")
if os.path.exists(note_path):
    with open(note_path, 'r') as f:
        print(f"\nContent of {note_path}:\n{f.read()}")

# --- Test AI-powered Scheduling ---
print("\n--- Testing AI-powered Scheduling ---")

# 1. Get AI response for a scheduling request
user_request = "remind me to call the electrician every weekday at 9am"
print(f"User request: '{user_request}'")
llm_response_str = get_llm_response(user_request)
print(f"AI response: {llm_response_str}")

# 2. Parse the response and schedule the job
cleaned_response = strip_markdown_fences(llm_response_str)
try:
    llm_response = json.loads(cleaned_response)
    if llm_response.get('function') == 'schedule_job':
        scheduler = Scheduler('schedule.json')
        args = llm_response.get('args', {})
        scheduler.schedule_job(args.get('text'), args.get('cron'))
        print("\nJob scheduled successfully.")
        # Allow a moment for the file to be written
        time.sleep(1)
        # 3. Verify schedule content
        if os.path.exists(scheduler.job_file):
            with open(scheduler.job_file, 'r') as f:
                print(f"\nContent of {scheduler.job_file}:\n{f.read()}")
    else:
        print("AI did not return a schedule_job function call.")
except json.JSONDecodeError:
    print(f"Error: Could not decode AI response as JSON: {llm_response_str}")
except Exception as e:
    print(f"An error occurred during scheduling: {e}")

# --- Cleanup ---
# You can uncomment these lines to clean up created files after testing
# os.remove(note_path)
# os.remove('schedule.json')
