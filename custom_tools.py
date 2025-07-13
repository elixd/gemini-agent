import os
import json
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from scheduler import Scheduler

# Clear schedule.json before instantiating the scheduler
if os.path.exists('schedule.json'):
    with open('schedule.json', 'w') as f:
        json.dump([], f)

# Instantiate the scheduler
scheduler = Scheduler('schedule.json')

class CreateNoteArgs(BaseModel):
    topic: str = Field(description="The topic of the note.")
    text: str = Field(description="The text of the note.")

class ReadNoteArgs(BaseModel):
    topic: str = Field(description="The topic of the note.")

class ScheduleJobArgs(BaseModel):
    text: str = Field(description="The text of the reminder.")
    cron_schedule: str = Field(description="The cron schedule for the reminder (e.g., '0 10 * * *' for 10 AM daily).")

class RemoveJobArgs(BaseModel):
    job_id: str = Field(description="The ID of the job to remove.")

class GetScheduledJobsArgs(BaseModel):
    pass

def create_note(topic: str, text: str) -> str:
    """Creates a new note with the given topic and text."""
    # Ensure the notes directory exists
    if not os.path.exists('notes'):
        os.makedirs('notes')
    
    file_name = f"{topic.replace(' ', '_')}.md" if not topic.endswith('.md') else topic
    file_path = os.path.join('notes', file_name)
    with open(file_path, "w") as f:
        f.write(text)
    return f"Note '{file_path}' created successfully."

def read_note(topic: str) -> str:
    """Reads the content of a note with the given topic."""
    file_name = f"{topic.replace(' ', '_')}.md" if not topic.endswith('.md') else topic
    file_path = os.path.join('notes', file_name)
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: Note '{file_path}' not found."

def schedule_job(text: str, cron_schedule: str) -> str:
    """Schedules a job for the agent to send a message to the user using a cron expression."""
    try:
        return scheduler.schedule_job(text, cron_schedule)
    except Exception as e:
        return f"Error scheduling job: {e}"

def remove_job(job_id: str) -> str:
    """Removes a scheduled job by its ID."""
    try:
        scheduler.remove_job(job_id)
        return f"Job {job_id} removed successfully."
    except Exception as e:
        return f"Error removing job: {e}"

def get_scheduled_jobs() -> str:
    """Returns a summary of all scheduled jobs."""
    return scheduler.get_dashboard_summary()

create_note_tool = StructuredTool.from_function(
    func=create_note,
    name="create_note",
    description="Creates a new note with a given topic and text.",
    args_schema=CreateNoteArgs
)

read_note_tool = StructuredTool.from_function(
    func=read_note,
    name="read_note",
    description="Reads the content of a note with the given topic.",
    args_schema=ReadNoteArgs
)

schedule_job_tool = StructuredTool.from_function(
    func=schedule_job,
    name="schedule_job",
    description="Schedules a job for the agent to send a message to the user.",
    args_schema=ScheduleJobArgs
)

remove_job_tool = StructuredTool.from_function(
    func=remove_job,
    name="remove_job",
    description="Removes a scheduled job by its ID.",
    args_schema=RemoveJobArgs
)

get_scheduled_jobs_tool = StructuredTool.from_function(
    func=get_scheduled_jobs,
    name="get_scheduled_jobs",
    description="Returns a summary of all scheduled jobs.",
    args_schema=GetScheduledJobsArgs
)