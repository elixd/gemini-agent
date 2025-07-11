# Example: Agent World Awareness Block

This file contains a concrete example of the full text block that our agent would receive for a specific request. It demonstrates the three-tier context architecture.

**Scenario:**
*   **User's Request:** "What's the status of the house project and should I add 'get paint samples' to the list?"
*   **Current State:** It's the afternoon of July 12, 2025. The user has a meeting and a dentist appointment tomorrow. The agent has one recurring task and one note file.

---

# TIER 1: UNCONDITIONAL CONTEXT (Always Provided)

## SYSTEM PROMPT (Static Part of Dashboard)
You are a proactive, context-aware personal AI assistant. Your primary goal is to help the user manage their life by understanding their schedule, tasks, and notes. You are conversational and have access to tools to help you.

## AVAILABLE TOOLS (Static Part of Dashboard)
- `create_note(topic: str)`: Creates a new note file.
- `update_note(topic: str, text: str)`: Appends text to an existing note.
- `schedule_job(text: str, cron: str)`: Schedules a recurring or one-time reminder.

## DYNAMIC DASHBOARD (Dynamic Part of Dashboard)
---
Current Time: 2025-07-12 14:30:00

Upcoming Calendar Events (Next 24h):
- 2025-07-13 10:00 - Team Meeting
- 2025-07-13 15:00 - Dentist Appointment

Scheduled Tasks:
- ID: e20b0a5e, Text: "call the electrician", Schedule: Every weekday at 09:00

Active Notes:
- house_project_test.md
---

# TIER 2: CONDITIONAL CONTEXT (Prepared by Briefing Assistant)

## CONTEXTUAL BRIEFING
The user's request mentions the "house project". The content of the relevant note file `house_project_test.md` has been retrieved to provide context:
---
# House Project Test

- Contacted architect
- Reviewed blueprints
---

# TIER 3: AGENT-DRIVEN CONTEXT (Populated during the agent's reasoning)

## AGENT SCRATCHPAD / CONTEXT FROM PRIOR ACTIONS
(This section is initially empty. It gets filled if the agent decides to use a tool. For example, if it chose to use `update_note` first, the result "Note 'house_project_test.md' updated." would appear here before its final response.)

# USER'S CURRENT REQUEST
What's the status of the house project and should I add 'get paint samples' to the list?
