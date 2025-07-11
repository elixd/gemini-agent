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

# --- Multi-Turn Scheduling Test ---

# Turn 1: User provides the reminder text
run_turn("Turn 1: Providing Reminder Text", "Remind me to call my mom")

# Turn 2: User provides the schedule in a separate message
run_turn("Turn 2: Providing Schedule", "Can you schedule that for tomorrow at 6pm?")

# --- Verification ---
print("\n--- Verifying Scheduled Jobs ---")
summary = scheduler.get_dashboard_summary()
print(summary)

# Final cleanup
for job in scheduler.scheduler.get_jobs():
    job.remove()
scheduler.save_jobs()
print("\nScheduled jobs cleaned up.")
