
from agent import run_agent
from scheduler import Scheduler

# Instantiate the scheduler
scheduler = Scheduler('schedule.json')

# Define the test input
user_input = "Create a note about my house project. The first task is to contact the architect."

# Invoke the agent
response = run_agent(user_input, scheduler)

# Print the final response
print("--- Agent Output ---")
print(response['output'])
print("--------------------")
