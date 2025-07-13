import os
import json
import pytest
from scheduler import Scheduler
from apscheduler.triggers.cron import CronTrigger

# Define a dummy job function for testing
def dummy_job_function(text):
    print(f"Test Reminder: {text}")

@pytest.fixture(scope="function")
def clean_scheduler():
    job_file = 'test_schedule.json'
    if os.path.exists(job_file):
        os.remove(job_file)
    scheduler = Scheduler(job_file)
    yield scheduler
    scheduler.shutdown()
    if os.path.exists(job_file):
        os.remove(job_file)

def test_schedule_and_save_job(clean_scheduler):
    scheduler = clean_scheduler
    text = "Follow up with the design team"
    cron_expression = "0 10 * * *"  # Every day at 10:00 AM

    # Schedule the job
    response = scheduler.schedule_job(text, cron_expression)
    assert response == "Job scheduled successfully."

    # Verify the job is saved correctly in the JSON file
    with open(scheduler.job_file, 'r') as f:
        jobs_data = json.load(f)
    
    assert len(jobs_data) == 1
    saved_job = jobs_data[0]
    assert saved_job['text'] == text
    assert saved_job['cron'] == cron_expression

def test_load_jobs(clean_scheduler):
    scheduler = clean_scheduler
    text = "Another reminder"
    cron_expression = "30 14 * * 1"  # Every Monday at 2:30 PM

    # Manually save a job to the file
    job_id = "test_job_id_123"
    job_data = [{'id': job_id, 'text': text, 'cron': cron_expression}]
    with open(scheduler.job_file, 'w') as f:
        json.dump(job_data, f, indent=4)
    
    # Create a new scheduler instance to load jobs from the file
    new_scheduler = Scheduler(scheduler.job_file)
    
    # Verify the job is loaded
    loaded_jobs = new_scheduler.scheduler.get_jobs()
    assert len(loaded_jobs) == 1
    loaded_job = loaded_jobs[0]
    assert loaded_job.args[0] == text
    assert isinstance(loaded_job.trigger, CronTrigger)
    assert loaded_job.kwargs['original_cron'] == cron_expression
    
    new_scheduler.shutdown()

def test_remove_job(clean_scheduler):
    scheduler = clean_scheduler
    text = "Job to be removed"
    cron_expression = "0 0 * * *"

    # Schedule a job
    scheduler.schedule_job(text, cron_expression)
    
    # Get the job ID
    jobs = scheduler.scheduler.get_jobs()
    assert len(jobs) == 1
    job_id = jobs[0].id

    # Remove the job
    scheduler.remove_job(job_id)

    # Verify no jobs are left
    assert len(scheduler.scheduler.get_jobs()) == 0
    with open(scheduler.job_file, 'r') as f:
        jobs_data = json.load(f)
    assert len(jobs_data) == 0
