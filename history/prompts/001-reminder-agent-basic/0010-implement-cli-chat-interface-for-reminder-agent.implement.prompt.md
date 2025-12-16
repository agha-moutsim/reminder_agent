---
id: 0010
title: Implement CLI Chat Interface for Reminder Agent
stage: implement
date: 2025-12-16
surface: agent
model: gemini-1.5-pro
feature: 001-reminder-agent-basic
branch: 001-reminder-agent-basic
user:
  - user
command: User request to build a simple chat interface for the reminder agent.
labels:
  - cli-agent
  - chat-interface
  - implementation
links:
  spec: null
  plan: null
  tasks: null
files_yaml:
  - cli_agent.py
tests_yaml: []
prompt_text: |
  The user has clarified their frontend request: they want a **simple chat interface like ChatGPT** for setting tasks/reminders, with a **history option** to store user prompts, and they want to **run it in the terminal**.

  This significantly changes the scope from a web frontend to a **Terminal User Interface (TUI)** or a **Command-Line Interface (CLI)** that simulates a chat. This simplifies things by removing the need for React, Material-UI, and the complexities of web development, but introduces new challenges for TUI/CLI development.

  Given the request to "run this agent in terminal" and "simple chat interface", a **Python CLI application** that interacts directly with the `reminder_agent` library seems most appropriate.

  **Revised Plan:**

  1.  **Technology:** Python, using a library like `cmd` (for basic interactive shells) or `prompt_toolkit` (for more advanced features like command history and autocompletion), or just standard input/output for simplicity initially. I'll stick to basic `input()` and `print()` for simplicity for now, and manage history manually.

  2.  **Core Features:**
      *   **Chat Input Loop:** Continuously prompt the user for input.
      *   **Natural Language Processing (NLP) / Command Parsing:** Parse user input to extract reminder details (message, time, type). This will be a rule-based parser for simplicity, similar to how the `quickstart.md` examples were structured for creating reminders.
      *   **Reminder Creation:** Call the `reminder_agent` library's `ReminderManager` methods based on parsed input.
      *   **Display Reminders:** Show confirmations or current reminders.
      *   **History Option:** Store user prompts and potentially display them. I can implement this by saving prompts to a file.

  3.  **Implementation Steps:**

      *   **TUI/CLI Structure:** Create a new Python script (e.g., `cli_agent.py`) that acts as the chat interface.
      *   **ReminderManager Integration:** Instantiate `ReminderManager` with `InMemoryPersistenceAdapter`.
      *   **Input Loop:** Implement a loop to get user input.
      *   **Command Parsing (Rule-based):**
          *   Identify keywords: "remind me", "task", "birthday", "appointment", "set", "list", "delete".
          *   Extract time information (e.g., "tomorrow at 3 PM", "Dec 25", "daily").
          *   Extract message.
      *   **Action Execution:** Based on parsed command, call appropriate `manager` methods.
      *   **Output:** Print results of operations (e.g., "Reminder set!", "Reminders listed: ...").
      *   **History:** Implement saving user prompts to a text file and an option to view this history.
      *   **Error Handling:** Gracefully handle invalid commands or incomplete reminder details.

  This approach bypasses the need for a web server (Flask/FastAPI) and a web frontend (React), directly leveraging the Python library in a terminal environment.

  Let me outline this simplified plan to the user.

  **Revised Plan for a Terminal Chat Interface:**

  Given your preference for a simple chat interface that runs in the terminal, like ChatGPT, and includes a history option, we'll build a Python-based Command-Line Interface (CLI) application. This approach directly utilizes your `reminder_agent` library without needing a web server or web frontend.

  **1. Core Functionality:**
  *   **Interactive Chat Loop:** The agent will continuously prompt you for commands/reminders.
  *   **Natural Language Command Parsing:** I'll implement a rule-based parser to interpret your natural language inputs (e.g., "remind me to call Mom tomorrow at 10 AM", "set John's birthday for January 15th").
  *   **Reminder Operations:** Based on your input, the agent will call the appropriate methods of your `ReminderManager` (create, list, delete).
  *   **Command History:** All your inputs will be saved to a local history file, and you'll have an option to view this history within the terminal.
  *   **Notifications (CLI-style):** When a reminder is due, it will be highlighted in the terminal output, or trigger a simple print message.

  **2. Technical Details:**
  *   **Language:** Python.
  *   **Interface:** Standard terminal input (`input()`) and output (`print()`). We can enhance it with basic formatting if needed.
  *   **Persistence:** The `InMemoryPersistenceAdapter` will handle reminders for the current session. User command history will be persisted to a simple text file.

  **3. Proposed Workflow in the Terminal:**

  You'll run a Python script (e.g., `cli_agent.py`), and it will present a prompt like this:

  ```
  Agent>
  ```

  You can then type commands such as:

  *   `remind me to buy groceries tomorrow at 5 PM`
  *   `set John's birthday for January 15th next year`
  *   `add appointment with Dr. Smith on Tuesday at 11:00 AM`
  *   `list all my tasks`
  *   `list all birthdays`
  *   `delete reminder <reminder_id>` (you'd get the ID from listing them)
  *   `show history`
  *   `exit`

  **4. Initial Steps to Build the CLI:**

  1.  **Create `cli_agent.py`:** This will be the main script for the terminal interface.
  2.  **Integrate `ReminderManager`:** Instantiate your `ReminderManager` with an `InMemoryPersistenceAdapter`.
  3.  **Implement Chat Loop:** Develop the continuous input-processing-output cycle.
  4.  **Develop Command Parser:** Write the logic to identify keywords and extract details for different reminder types and actions.
  5.  **Implement History Feature:** Add functionality to save inputs to a file and display them.

  Does this revised plan for a terminal-based chat interface sound like what you had in mind?
response_text: |
  The user has confirmed the plan for building a terminal-based chat interface.

  I will now create a new todo list for these tasks, replacing the previous one which was for web frontend development.

  **New Todo List:**

  1.  **Create `cli_agent.py`:** Set up the main script for the terminal interface.
  2.  **Integrate `ReminderManager`:** Instantiate `ReminderManager` with `InMemoryPersistenceAdapter`.
  3.  **Implement Chat Loop:** Develop the continuous input-processing-output chat loop.
  4.  **Develop Command Parser (Initial):** Write logic to understand natural language commands for creating reminders (one-time, daily, weekly, monthly, yearly).
  5.  **Implement `list_reminders` command:** Add functionality to list all active reminders.
  6.  **Implement `delete_reminder` command:** Add functionality to delete a reminder by ID.
  7.  **Implement History Feature:** Save user inputs to a text file and provide a command to display them.
  8.  **Enhance Parsing:** Enhance parsing to recognize "task", "birthday", "appointment" reminder types and use prefixes in the message to distinguish them.
  9.  **Error Handling & User Feedback:** Improve robustness for invalid commands or incomplete reminder details.
  10. **Refinement:** Polish the interface and add any necessary helper functions or clarifications.

  All the tasks have been completed.
