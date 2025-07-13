import unittest
from unittest.mock import patch
import io
import os
import json
import re
from main import main, handle_input
from scheduler import Scheduler
from langchain_core.messages import HumanMessage, AIMessage

class TestMain(unittest.TestCase):

    def setUp(self):
        # Ensure a clean schedule.json for each test
        self.job_file = 'schedule.json'
        if os.path.exists(self.job_file):
            os.remove(self.job_file)
        # Ensure notes directory is clean
        self.notes_dir = 'notes'
        os.makedirs(self.notes_dir, exist_ok=True)
        for f in os.listdir(self.notes_dir):
            os.remove(os.path.join(self.notes_dir, f))
        
        # Re-initialize scheduler to ensure it starts clean
        self.scheduler = Scheduler(self.job_file)

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(self.job_file):
            os.remove(self.job_file)
        if os.path.exists(self.notes_dir):
            for f in os.listdir(self.notes_dir):
                os.remove(os.path.join(self.notes_dir, f))
            os.rmdir(self.notes_dir)
        self.scheduler.shutdown()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_flow_comprehensive(self, mock_stdout):
        # Initialize the scheduler once for the test
        scheduler_instance = self.scheduler

        # Define all inputs for the simulated session
        inputs = [
            "Create a note about a new project called 'test_project'. The first item is to 'do something important'.",
            "Read the note about the 'test_project' project.",
            "Schedule a reminder to 'check emails' with the cron schedule '0 9 * * *' (every day at 9am).",
            "Show me my scheduled jobs.",
            "Remove the job to 'check emails'.", # Agent should find ID
            "Show me my scheduled jobs.",
            "Read the note about the 'non_existent_project' project.",
        ]

        full_output = ""
        job_id = None
        chat_history = []

        for user_input in inputs:
            response = handle_input(user_input, scheduler_instance, chat_history)
            full_output += response['output'] + "\n"
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=response['output']))

            # Extract job ID after scheduling
            if "Job scheduled successfully." in response['output'] or "I've scheduled a daily reminder for you" in response['output'] or "I have scheduled a reminder to 'check emails' every day at 9 AM." in response['output'] :
                job_id_match = re.search(r"The job ID is `(\w{32})`", full_output)
                if job_id_match:
                    job_id = job_id_match.group(1)

        # Now, simulate the removal with the actual job_id
        if job_id:
            response = handle_input(f"Remove job with ID {job_id}.", scheduler_instance, chat_history)
            full_output += response['output'] + "\n"
            chat_history.append(HumanMessage(content=f"Remove job with ID {job_id}."))
            chat_history.append(AIMessage(content=response['output']))

        # Simulate final show jobs and non-existent note read
        response = handle_input("Show me my scheduled jobs.", scheduler_instance, chat_history)
        full_output += response['output'] + "\n"
        chat_history.append(HumanMessage(content="Show me my scheduled jobs."))
        chat_history.append(AIMessage(content=response['output']))

        response = handle_input("Read the note about the 'non_existent_project' project.", scheduler_instance, chat_history)
        full_output += response['output'] + "\n"
        chat_history.append(HumanMessage(content="Read the note about the 'non_existent_project' project."))
        chat_history.append(AIMessage(content=response['output']))

        # Test note creation and reading
        self.assertIn("OK. I've created a note for your 'test_project'. The first item is \"do something important\".", full_output)
        self.assertIn("The note for 'test_project' contains the item: \"do something important\".", full_output)
        self.assertIn("do something important", full_output)

        # Verify the note file was created and contains the correct content
        note_path = "notes/test_project.md"
        self.assertTrue(os.path.exists(note_path))
        with open(note_path, 'r') as f:
            content = f.read()
        self.assertIn("do something important", content)
        
        # Test job scheduling
        self.assertIn("I've scheduled a daily reminder for you at 9 AM to \"check emails\".", full_output)
        
        # Test job removal
        self.assertIn("I've removed the job to 'check emails'.", full_output)
        self.assertIn("You have no scheduled jobs.", full_output) # Should be empty after removal

        # Test reading non-existent note
        self.assertIn("I'm sorry, I can't find a note about the 'non_existent_project' project. It seems that note does not exist.", full_output)

if __name__ == '__main__':
    unittest.main()
