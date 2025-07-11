from agent import agent_executor, scheduler
from dashboard import build_dashboard_context

print("--- Testing Conversational Memory ---")

# Turn 1: Give the agent a piece of information to remember
print("\n--- Turn 1: Stating a fact ---")
user_input_1 = "Please remember that my name is Ilya."
dashboard_1 = build_dashboard_context(scheduler)
augmented_input_1 = f"{dashboard_1}\n\nUser Request: {user_input_1}"

print(f"Invoking agent with: '{user_input_1}'")
response_1 = agent_executor.invoke({"input": augmented_input_1})
print(f"Agent Response: {response_1['output']}")

# Turn 2: Ask a question that relies on the previous turn
print("\n--- Turn 2: Asking a question ---")
user_input_2 = "What is my name?"
dashboard_2 = build_dashboard_context(scheduler)
augmented_input_2 = f"{dashboard_2}\n\nUser Request: {user_input_2}"

print(f"Invoking agent with: '{user_input_2}'")
response_2 = agent_executor.invoke({"input": augmented_input_2})

print("\n--- Agent's Final Response (Demonstrating Memory) ---")
print(response_2["output"])
