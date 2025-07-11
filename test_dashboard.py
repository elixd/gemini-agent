import time
from agent import agent_executor, scheduler
from dashboard import build_dashboard_context

print("--- Testing Dashboard Awareness ---")

# 1. Ensure a task exists for the dashboard.
# First, remove any old jobs to ensure a clean state.
for job in scheduler.scheduler.get_jobs():
    job.remove()
scheduler.save_jobs()

# Now, add a new one.
print("Scheduling a test task...")
scheduler.schedule_job(text="Review the agent's new dashboard feature", cron="* * * * *") # Every minute
time.sleep(1) # Allow scheduler to process

# 2. Define a user question that requires dashboard knowledge.
user_question = "What do I have scheduled right now?"
print(f"\nSimulating user request: '{user_question}'")

# 3. Build the dashboard and invoke the agent.
dashboard = build_dashboard_context(scheduler)
augmented_input = f"{dashboard}\n\nUser Request: {user_question}"

print("\nInvoking agent with the following augmented input:")
print("--------------------------------------------------")
print(augmented_input)
print("--------------------------------------------------")

response = agent_executor.invoke({"input": augmented_input})

print("\n--- Agent's Final Response ---")
print(response["output"])

# Clean up the test job
for job in scheduler.scheduler.get_jobs():
    job.remove()
scheduler.save_jobs()
print("\nTest task cleaned up.")
