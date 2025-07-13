import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError



def job_function(text, **kwargs):
    print(f"REMINDER: {text}")

class Scheduler:
    def __init__(self, job_file):
        self.scheduler = BackgroundScheduler()
        self.job_file = job_file
        self.load_jobs()
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def schedule_job(self, text: str, cron_expression: str) -> str:
        """Schedules a job for the agent to send a message to the user. The `text` should be the full content of the reminder. The `cron_expression` should be a valid cron string (e.g., '0 10 * * *' for 10 AM daily)."""
        self.scheduler.add_job(job_function, CronTrigger.from_crontab(cron_expression), args=[text], kwargs={'original_cron': cron_expression})
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
            jobs.append({'id': job.id, 'text': job.args[0], 'cron': job.kwargs['original_cron']})
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
                    self.scheduler.add_job(job_function, CronTrigger.from_crontab(job['cron']), args=[job['text']], id=job['id'], kwargs={'original_cron': job['cron']})
            
        except FileNotFoundError:
            print("[DEBUG] No job file found.")
            pass
