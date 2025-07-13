import os
import json
from agent import run_agent
from scheduler import Scheduler

# Clear schedule.json before tests run to ensure a clean state
if os.path.exists('schedule.json'):
    with open('schedule.json', 'w') as f:
        json.dump([], f)

# Instantiate the scheduler
scheduler = Scheduler('schedule.json')

def test_create_note():
    print("--- Testing create_note ---")
    user_input = "Create a note about a new project called 'marketing_campaign'. The first item is to 'design a new logo'."
    response = run_agent(user_input, scheduler)
    print(f"Agent Output: {response['output']}")
    assert os.path.exists("notes/marketing_campaign.md"), "Test Failed: Note was not created."
    print("Test Passed: Note was created successfully.")

def test_read_note():
    print("\n--- Testing read_note ---")
    user_input = "Read the note about the 'marketing_campaign' project."
    response = run_agent(user_input, scheduler)
    print(f"Agent Output: {response['output']}")
    with open("notes/marketing_campaign.md", "r") as f:
        content = f.read()
    assert "design a new logo" in content, "Test Failed: Note content is incorrect."
    print("Test Passed: Note was read successfully.")

import json

def test_schedule_job():
    print("\n--- Testing schedule_job ---")
    # Clear existing jobs before testing
    with open(scheduler.job_file, 'w') as f:
        json.dump([], f)
    scheduler.load_jobs() # Reload empty jobs

    user_input = "Schedule a reminder to 'follow up with the design team' with the cron schedule '0 10 * * *' (every day at 10am)."
    response = run_agent(user_input, scheduler)
    print(f"Agent Output: {response['output']}")

    # Verify the job is in the schedule.json file
    with open(scheduler.job_file, 'r') as f:
        jobs = json.load(f)
    
    found_job = False
    for job in jobs:
        if "follow up with the design team" in job['text'] and job['cron'] == '0 10 * * *' :
            found_job = True
            break
    assert found_job, "Test Failed: Job was not scheduled correctly in schedule.json."
    print("Test Passed: Job was scheduled successfully.")

if __name__ == "__main__":
    test_create_note()
    test_read_note()
    test_schedule_job()
    print("\n--- All tests passed! ---")