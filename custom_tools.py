
from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class ScheduleJobInput(BaseModel):
    schedule: str = Field(description="A human-readable schedule string (e.g., 'every hour', 'every day at 5pm').")

class ScheduleJobTool(BaseTool):
    name: str = "schedule_job"
    description: str = "Schedules a job for the agent to send a message to the user at a specific time. The user's original prompt will be used as the reminder text."
    args_schema: Type[BaseModel] = ScheduleJobInput
    scheduler: object

    def _run(self, schedule: str, user_prompt: str):
        return self.scheduler.schedule_job(schedule, user_prompt)
