import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError

from time_utils import parse_schedule


def job_function(text):
    print(f"REMINDER: {text}")

class Scheduler:
    def __init__(self, job_file):
        self.scheduler = BackgroundScheduler()
        self.job_file = job_file
        self.load_jobs()
        self.scheduler.start()

    def schedule_job(self, text: str, schedule: str) -> str:
        """Schedules a job for the agent to send a message to the user. The `text` should be the full content of the reminder. The `schedule` should be a human-readable schedule string (e.g., 'every hour', 'tomorrow at 5pm')."""
        cron_expression = parse_schedule(schedule)
        if not cron_expression:
            return f"Error: Could not parse schedule string: '{schedule}'"
        
        self.scheduler.add_job(job_function, CronTrigger.from_crontab(cron_expression), args=[text])
        self.save_jobs()
        return "Job scheduled successfully."

    def remove_job(self, job_id):
        try:
            self.scheduler.remove_job(job_id)
            self.save_jobs()
        except JobLookupError:
            print(f"Job with id {job_id} not found.")

    def save_jobs(self):
        jobs = []
        for job in self.scheduler.get_jobs():
            # Explicitly get minute, hour, day_of_month, month, day_of_week
            cron_str = f"{job.trigger.fields[0]} {job.trigger.fields[1]} {job.trigger.fields[2]} {job.trigger.fields[3]} {job.trigger.fields[4]}"
            jobs.append({'id': job.id, 'text': job.args[0], 'cron': cron_str})
        with open(self.job_file, 'w') as f:
            json.dump(jobs, f, indent=4)

    def get_dashboard_summary(self):
        """Returns a summary of all scheduled jobs for display in the dashboard."""
        summary = []
        for job in self.scheduler.get_jobs():
            summary.append(f"- ID: {job.id}, Text: {job.args[0]}, Schedule: {job.trigger}")
        return "\n".join(summary) if summary else "No agent jobs scheduled."

    def load_jobs(self):
        try:
            with open(self.job_file, 'r') as f:
                jobs = json.load(f)
                for job in jobs:
                    self.scheduler.add_job(job_function, CronTrigger.from_crontab(job['cron']), args=[job['text']], id=job['id'])
        except FileNotFoundError:
            pass