
from agent import agent_executor, scheduler
from dashboard import build_dashboard_context

def main():
    print("Welcome to your personal AI agent. Type 'exit' to quit.")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        
        dashboard = build_dashboard_context(scheduler)
        augmented_input = f"{dashboard}\n\nUser Request: {user_input}"
        
        response = agent_executor.invoke({"input": augmented_input}, tool_run_kwargs={"user_prompt": user_input})
        print(response["output"])

if __name__ == "__main__":
    main()
