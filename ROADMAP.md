# Agent Development Roadmap

This document outlines the planned features and architectural milestones for our personal AI agent. It is a living document that will be updated as the project evolves.

## Milestone 1: Core Functionality (Complete)

- [x] Basic CLI interface.
- [x] Note-taking capabilities (`create_note`, `update_note`).
- [x] Agent-driven job scheduling (`schedule_job`).
- [x] Refactored to LangChain agent architecture.
- [x] Foundational "Dynamic Dashboard" (Tier 1) providing awareness of scheduled jobs and notes.
- [x] Conversational memory.
- [x] Robust toolset (`list_notes`, `read_note`) and error handling.
- [x] Semantic clarification to distinguish between agent jobs and user tasks.

## Milestone 2: Advanced Contextual Awareness

- [ ] **Implement the "Briefing Assistant" (Tier 2):** Create a dedicated chain or function that analyzes the user's prompt and pre-fetches relevant context (e.g., reading a note file if its topic is mentioned) *before* the main agent is called.
- [ ] **Integrate with External Services (Read-Only):**
    - [ ] Google Calendar API: Give the agent the ability to read the user's calendar to provide proactive advice and check for conflicts.
    - [ ] Todoist or Google Tasks API: Allow the agent to read the user's personal to-do list to provide a more holistic view of their day.

## Milestone 3: Proactive Agent Capabilities

- [ ] **Implement the Proactive "Heartbeat" Loop:** Refactor the main application loop to be asynchronous (`asyncio`). Create a background task that runs every minute or so, allowing the agent to trigger actions on its own based on the current time and state.
    - *Use Case:* Proactively remind the user of an upcoming meeting without being prompted.
    - *Use Case:* Pre-fetch and summarize relevant notes before a scheduled event.

## Milestone 4: Enhanced Modalities

- [ ] **Telegram Bot Interface:** Wrap the agent's core logic in a `python-telegram-bot` interface to make it accessible from mobile devices.
- [ ] **Voice Interaction (Future):** Explore options for speech-to-text and text-to-speech to enable hands-free interaction.
