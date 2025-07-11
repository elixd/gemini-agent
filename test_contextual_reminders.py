from agent import agent_executor, scheduler
from dashboard import build_dashboard_context

def run_turn(turn_name, user_input):
    print(f"\n--- {turn_name} ---")
    dashboard = build_dashboard_context(scheduler)
    augmented_input = f"{dashboard}\n\nUser Request: {user_input}"
    print(f"User Request: '{user_input}'")
    response = agent_executor.invoke({"input": augmented_input})
    print(f"Agent Response: {response['output']}")
    return response['output']

# Clean up any old jobs first
for job in scheduler.scheduler.get_jobs():
    job.remove()
scheduler.save_jobs()

# --- Test Scenario ---

# Turn 1: User schedules a reminder
run_turn("Turn 1: Scheduling a Reminder", "can you remind me to call my client tomorrow")

# Turn 2: User asks to see the scheduled jobs
run_turn("Turn 2: Listing Scheduled Jobs", "show your jobs")

# --- Verification ---
print("\n--- Verifying Scheduled Jobs ---")
summary = scheduler.get_dashboard_summary()
print(summary)

# Final cleanup
for job in scheduler.scheduler.get_jobs():
    job.remove()
scheduler.save_jobs()
print("\nScheduled jobs cleaned up.")
