from agent import agent_executor, scheduler
from dashboard import build_dashboard_context

def run_turn(turn_name, user_input):
    print(f"\n--- {turn_name} ---")
    dashboard = build_dashboard_context(scheduler)
    augmented_input = f"{dashboard}\n\nUser Request: {user_input}"
    print(f"User Request: '{user_input}'")
    response = agent_executor.invoke({"input": augmented_input, "user_input": user_input})
    print(f"Agent Response: {response['output']}")
    return response['output']

# Clean up any old jobs first
for job in scheduler.scheduler.get_jobs():
    job.remove()
scheduler.save_jobs()

# --- Test Scenarios from Dialogue ---

# Scenario 1: Relative time
run_turn("Scenario 1: Relative Time", "remind me to brush my teeth in one day")

# Scenario 2: Specific time tomorrow
run_turn("Scenario 2: Specific Time Tomorrow", "remind me to call the bank tomorrow at 10am")

# Scenario 3: Recurring daily task
run_turn("Scenario 3: Recurring Daily Task", "remind me to do a daily review every day at 8pm")

# --- Verification ---
print("\n--- Verifying Scheduled Jobs ---")
summary = scheduler.get_jobs_summary()
print(summary)

# Final cleanup
for job in scheduler.scheduler.get_jobs():
    job.remove()
scheduler.save_jobs()
print("\nScheduled jobs cleaned up.")
