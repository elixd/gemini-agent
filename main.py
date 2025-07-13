import os
from agent import run_agent
from scheduler import Scheduler
from langchain_core.messages import HumanMessage, AIMessage

scheduler = Scheduler('schedule.json')

def handle_input(user_input, scheduler, chat_history):
    return run_agent(user_input, scheduler, chat_history)

def main():
    print("Welcome to your personal AI agent. Type 'exit' to quit.")
    # Ensure the notes directory exists
    os.makedirs('notes', exist_ok=True)

    chat_history = []

    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        
        response = handle_input(user_input, scheduler, chat_history)
        print(response['output'])
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response['output']))

if __name__ == "__main__":
    main()