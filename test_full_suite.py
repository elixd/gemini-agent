

import os
from agent import agent_executor, scheduler
from dashboard import build_dashboard_context

# --- Test Setup ---
print("--- Test Setup ---")
NOTE_TOPIC = "test_note"
NOTE_FILE = f"notes/{NOTE_TOPIC}.md"

# 1. Create a dummy note file
with open(NOTE_FILE, "w") as f:
    f.write("# This is a test note.\n")
print(f"Created dummy note: {NOTE_FILE}")

# --- Test Execution ---
def run_turn(turn_name, user_input):
    print(f"\n--- {turn_name} ---")
    dashboard = build_dashboard_context(scheduler)
    augmented_input = f"{dashboard}\n\nUser Request: {user_input}"
    print(f"User Request: '{user_input}'")
    response = agent_executor.invoke({"input": augmented_input})
    print(f"Agent Response: {response['output']}")
    return response['output']

# Turn 1: Verify list_notes tool
run_turn("Turn 1: Listing Notes", "What notes do I have?")

# Turn 2: Verify read_note tool
run_turn("Turn 2: Reading a Note", f"Read the {NOTE_TOPIC} note")

# Turn 3: Verify enhanced error handling
run_turn("Turn 3: Testing Error Handling", "Add 'test' to the non_existent_note")

# Turn 4: Verify scheduling with new semantics
run_turn("Turn 4: Scheduling an Agent Job", "schedule a job to remind me to check my email every hour")

# --- Test Cleanup ---
print("\n--- Test Cleanup ---")
os.remove(NOTE_FILE)
print(f"Removed dummy note: {NOTE_FILE}")
# Clean up any scheduled jobs
for job in scheduler.scheduler.get_jobs():
    job.remove()
scheduler.save_jobs()
print("Scheduled jobs cleaned up.")

