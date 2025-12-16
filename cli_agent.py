import sys
import re
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import os
import threading
import time  # For time.sleep in the alert thread

from reminder_agent.core import ReminderManager
from reminder_agent.persistence import InMemoryPersistenceAdapter
from reminder_agent.models import Reminder, ReminderType


# Helper function to parse time expressions
# This function aims to be robust but is a simplification of full NLP.
def parse_time_expression(text: str) -> Optional[datetime]:
    now_utc = datetime.now(timezone.utc)

    # Remove common conversational noise to focus on date/time elements
    clean_text = re.sub(
        r"(?:remind(?:s)?\s+me|i have a|i need to)\s*", "", text, flags=re.IGNORECASE
    ).strip()

    # --- Absolute Date/Time Parsing ---

    # Pattern: YYYY-MM-DD HH:MM (e.g., "2025-12-31 23:59")
    match_full_dt = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}})", clean_text)
    if match_full_dt:
        try:
            dt_obj = datetime.strptime(match_full_dt.group(1), "%Y-%m-%d %H:%M").replace(
                tzinfo=timezone.utc
            )
            if dt_obj > now_utc:
                return dt_obj
        except ValueError:
            pass

    # Pattern: Month Day [Year] [HH:MM AM/PM] (e.g., "Jan 15 2026 9 PM", "Dec 25 10:30am", "March 3")
    match_month_day_time = re.search(
        r"(?:on|at|by)?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:\w*)\s+(\d{1,2})(?:\s+(\d{4}))?(?:\s+(?:at|by)\s+(\d{1,2}(?:\:\d{2})?\s*(?:AM|PM)?))?",
        clean_text,
        re.IGNORECASE,
    )
    if match_month_day_time:
        try:
            month_str = match_month_day_time.group(1)
            day = int(match_month_day_time.group(2))
            year = (
                int(match_month_day_time.group(3))
                if match_month_day_time.group(3)
                else now_utc.year
            )
            time_str_raw = match_month_day_time.group(4)  # Can be None

            month_num = datetime.strptime(month_str[:3], "%b").month  # Use [:3] for robustness

            # Default to 9 AM if no time is specified, and construct a full time string
            effective_time_str = time_str_raw if time_str_raw else "9 AM"

            # Parse effective_time_str to get hour and minute
            parsed_hour = 9
            parsed_minute = 0

            time_parts_match = re.search(
                r"(\d{1,2})(?:\:(\d{2}))?\s*(am|pm)",
                effective_time_str.replace(" ", ""),
                re.IGNORECASE,
            )
            if time_parts_match:
                parsed_hour = int(time_parts_match.group(1))
                if time_parts_match.group(2):  # minutes present
                    parsed_minute = int(time_parts_match.group(2))
                ampm = time_parts_match.group(3).lower()
                if ampm == "pm" and parsed_hour != 12:
                    parsed_hour += 12
                if ampm == "am" and parsed_hour == 12:
                    parsed_hour = 0  # 12 AM is midnight

            dt_obj = datetime(year, month_num, day, parsed_hour, parsed_minute, tzinfo=timezone.utc)

            # Adjust year if date is in the past and no year was specified
            if dt_obj < now_utc and not match_month_day_time.group(3):
                dt_obj = dt_obj.replace(year=dt_obj.year + 1)

            if dt_obj > now_utc:
                return dt_obj
        except ValueError:
            pass

    # --- Relative Date/Time Parsing ---

    # Pattern: "tomorrow at 3pm", "today 5:30pm"
    day_offset = None
    if "tomorrow" in clean_text.lower():
        day_offset = 1
    elif "today" in clean_text.lower():
        day_offset = 0

    if day_offset is not None:
        target_date = (now_utc + timedelta(days=day_offset)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        time_match = re.search(
            r"(?:at|by)?\s*(\d{1,2}(?:\:\d{2})?\s*(?:AM|PM)?)", clean_text, re.IGNORECASE
        )

        if time_match:
            try:
                time_str = time_match.group(1).replace(" ", "")
                parsed_hour = 0
                parsed_minute = 0
                time_parts_match = re.match(
                    r"(\d{1,2})(?:\:(\d{2}))?\s*(am|pm)", time_str, re.IGNORECASE
                )
                if time_parts_match:
                    parsed_hour = int(time_parts_match.group(1))
                    if time_parts_match.group(2):
                        parsed_minute = int(time_parts_match.group(2))
                    ampm = time_parts_match.group(3).lower()
                    if ampm == "pm" and parsed_hour != 12:
                        parsed_hour += 12
                    if ampm == "am" and parsed_hour == 12:
                        parsed_hour = 0
                else:  # Fallback if time is just a number
                    number_match = re.search(r"(\d{1,2})", time_str)
                    if number_match:
                        parsed_hour = int(number_match.group(1))
                        if (
                            parsed_hour < now_utc.hour and day_offset == 0
                        ):  # If it's today and hour is past
                            parsed_hour += 12  # Assume PM
                        if parsed_hour < 7:  # If hour is very early, assume PM too
                            parsed_hour += 12

                dt_obj = target_date.replace(
                    hour=parsed_hour, minute=parsed_minute, second=0, microsecond=0
                )

                # If parsed time is in the past for today, assume next day
                if dt_obj <= now_utc and day_offset == 0:
                    dt_obj += timedelta(days=1)

                if dt_obj > now_utc:
                    return dt_obj
            except (ValueError, AttributeError):
                pass

        # If "tomorrow" or "today" but no specific time, default to 9 AM tomorrow/today
        default_time = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
        if default_time <= now_utc:  # If 9 AM is in the past, default to 1 hour from now
            return (now_utc + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        return default_time

    # Pattern: "in X minutes/hours/days"
    if "in " in clean_text.lower():
        match_minutes = re.search(r"in (\d+) min(?:ute)?s?", clean_text, re.IGNORECASE)
        if match_minutes:
            return now_utc + timedelta(minutes=int(match_minutes.group(1)))
        match_hours = re.search(r"in (\d+) hour(?:s)?", clean_text, re.IGNORECASE)
        if match_hours:
            return now_utc + timedelta(hours=int(match_hours.group(1)))
        match_days = re.search(r"in (\d+) day(?:s)?", clean_text, re.IGNORECASE)
        if match_days:
            return now_utc + timedelta(days=int(match_days.group(1)))

    # Fallback: 1 hour from now if no time can be parsed
    print(f"DEBUG: Could not parse time from '{text}'. Defaulting to 1 hour from now.")
    return (now_utc + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)


class CLIAgent:
    HISTORY_FILE = ".agent_history.txt"
    ALERT_CHECK_INTERVAL = 5  # seconds

    def __init__(self):
        self.persistence_adapter = InMemoryPersistenceAdapter()
        self.manager = ReminderManager(self.persistence_adapter)
        self.history: List[str] = self._load_history()
        self.alert_thread = None
        self.running = False

    def _load_history(self) -> List[str]:
        if os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE, "r") as f:
                return [line.strip() for line in f if line.strip()]
        return []

    def _save_history(self):
        with open(self.HISTORY_FILE, "w") as f:
            for item in self.history:
                f.write(item + "\n")

    def _log_conversation(self, role: str, message: str):
        """Logs both user input and agent response to history."""
        self.history.append(f"{role}> {message}")

    def _alert_monitor(self):
        while self.running:
            now_utc = datetime.now(timezone.utc)

            # Get all reminders that haven't been deleted yet
            all_reminders = self.manager.list_reminders(include_past=True)

            for reminder in all_reminders:
                if reminder.scheduled_time <= now_utc:
                    # Trigger the callback manager's function for due reminders
                    # The manager itself will print the alert message
                    self.manager._callback_manager.trigger_callbacks(reminder)

                    # For one-time reminders, delete them after alerting
                    if reminder.type == ReminderType.ONE_TIME:
                        self.manager.delete_reminder(reminder.id)
                    # For recurring reminders, a real app would calculate the next occurrence
                    # and update the scheduled_time. For this simple demo, they will keep alerting.

            time.sleep(self.ALERT_CHECK_INTERVAL)

    def run(self):
        print("Welcome to the Reminder Agent CLI!")
        print("Type 'help' for available commands, 'exit' to quit.")

        self.running = True
        self.alert_thread = threading.Thread(target=self._alert_monitor, daemon=True)
        self.alert_thread.start()

        while True:
            try:
                user_input = input("Agent> ").strip()
                self._log_conversation("User", user_input)  # Log user input

                if user_input.lower() == "exit":
                    self.running = False  # Signal alert thread to stop
                    self._save_history()  # Save history before exiting
                    print("Goodbye!")
                    break
                elif user_input.lower() == "help":
                    self._display_help()
                elif user_input.lower() == "show history" or user_input.lower() == "h":
                    self._display_history()
                else:
                    self._process_command(user_input)

            except EOFError:
                self.running = False  # Signal alert thread to stop
                self._save_history()  # Save history before exiting on EOF
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                self._log_conversation("Agent", f"An unexpected error occurred: {e}")  # Log error

    def _display_help(self):
        help_message = """
Available Commands:
  - 'remind me to <message> <time_expression>' (e.g., 'remind me to buy milk tomorrow at 8 AM')
  - 'set <type> reminder <message> <time_expression>' (e.g., 'set birthday reminder for John on Jan 15 at 9 AM')
  - 'list all reminders', 'list', or 'l'
  - 'list (task|birthday|appointment) reminders'
  - 'delete reminder <id_prefix>'
  - 'show history' or 'h'
  - 'help': Display this help message
  - 'exit': Quit the agent
"""
        print(help_message)
        self._log_conversation("Agent", help_message)  # Log agent's help message

    def _display_history(self):
        if self.history:
            response = "\n--- Command History ---\n"
            for i, item in enumerate(self.history):
                response += f"{i+1}. {item}\n"
            response += "-----------------------"
            print(response)
        else:
            response = "History is empty."
            print(response)
        self._log_conversation("Agent", response)  # Log history content

    def _perform_delete(self, reminder_id_prefix):
        # Find the full ID based on the prefix
        matching_reminders = [
            r
            for r in self.manager.list_reminders(include_past=True)
            if r.id.startswith(reminder_id_prefix)
        ]

        response = ""
        if len(matching_reminders) == 1:
            full_id = matching_reminders[0].id
            if self.manager.delete_reminder(full_id):
                response = f"Reminder with ID '{reminder_id_prefix}...' deleted."
            else:
                response = f"Failed to delete reminder with ID '{reminder_id_prefix}...'."
        elif len(matching_reminders) > 1:
            response = f"Multiple reminders match '{reminder_id_prefix}...'. Please provide a more specific ID."
        else:
            response = f"No reminder found with ID starting with '{reminder_id_prefix}'."
        return response

    def _handle_conversation(self, text: str) -> Optional[str]:
        """Simple rule-based conversation handler."""
        text_lower = text.lower()

        greetings = ["hello", "hi", "hey", "good morning", "good evening", "greetings"]
        if any(greet in text_lower for greet in greetings):
            return "Hello! I'm your Reminder Agent. How can I help you organize your day?"

        if "how are you" in text_lower:
            return "I'm functioning perfectly and ready to help you set reminders!"

        if "who are you" in text_lower or "what are you" in text_lower:
            return "I am a CLI Reminder Agent designed to help you track tasks and appointments."

        if "thank" in text_lower:
            return "You're welcome!"

        if "bye" in text_lower or "see ya" in text_lower:
            return "Goodbye! Have a great day."

        return None

    def _process_command(self, command):
        command_lower = command.lower()

        response = ""  # To capture agent's response for logging

        # Handle specific commands first (delete, list)
        match_delete = re.match(r"delete reminder (\w+)", command_lower)
        if match_delete:
            reminder_id_prefix = match_delete.group(1)
            response = self._perform_delete(reminder_id_prefix)
            print(response)
            self._log_conversation("Agent", response)
            return

        # Handle 'delete' without ID interactively
        if command_lower == "delete" or command_lower == "delete reminder":
            print("Please provide the ID of the reminder you want to delete:")
            reminder_id_prefix = input("Delete ID> ").strip()
            self._log_conversation(
                "Agent", "Please provide the ID of the reminder you want to delete:"
            )
            self._log_conversation("User", reminder_id_prefix)

            if reminder_id_prefix:
                response = self._perform_delete(reminder_id_prefix)
            else:
                response = "Deletion cancelled."

            print(response)
            self._log_conversation("Agent", response)
            return

        if (
            command_lower.startswith("list all reminders")
            or command_lower == "list"
            or command_lower == "show me list"
            or command_lower == "l"
        ):
            reminders = self.manager.list_reminders(include_past=True)  # Include past for full list
            if reminders:
                response += "\n--- Your Reminders ---\n"
                for r in reminders:
                    response += f"ID: {r.id[:8]}..., Message: '{r.message}', Due: {r.scheduled_time}, Type: {r.type.value}\n"
                response += "----------------------"
            else:
                response = "No reminders found."
            print(response)
            self._log_conversation("Agent", response)
            return

        match_list_type = re.match(r"list (task|birthday|appointment) reminders", command_lower)
        if match_list_type:
            requested_type = match_list_type.group(1).upper()
            reminders = [
                r
                for r in self.manager.list_reminders(include_past=True)
                if requested_type in r.message.upper()
            ]
            if reminders:
                response += f"\n--- Your {requested_type.capitalize()} Reminders ---\n"
                for r in reminders:
                    response += f"ID: {r.id[:8]}..., Message: '{r.message}', Due: {r.scheduled_time}, Type: {r.type.value}\n"
                response += "----------------------"
            else:
                response = f"No {requested_type} reminders found."
            print(response)
            self._log_conversation("Agent", response)
            return

        # --- Flexible Reminder Creation Parsing ---
        message = ""
        time_expression_text = ""
        reminder_type_alias = None  # Default to one-time

        # Comprehensive pattern for one-time and simple recurring reminders
        # Catches phrases like:
        # "i have a dinner tomorrow at 8pm remind me"
        # "remind me to buy groceries on Dec 25 at 10 AM"
        # "tournament tomorrow at 3pm"
        # "set task finish report by tomorrow 5pm"
        match_flexible_remind = re.search(
            r"^(?:(?:set\s+(task|birthday|appointment)\s+reminder|remind me to|i have a|i need to)\s+)?(.+?)"  # Optional prefix, then message
            r"(?:\s+(?:on|at|in|by|for)\s+(.+?))?"  # Optional time phrase with preposition
            r"(?:\s+remind(?:s)?\s+me)?$",  # Optional "remind me" at the end
            command_lower,
        )

        if match_flexible_remind:
            # Extract type if present in "set <type> reminder"
            extracted_type = match_flexible_remind.group(1)
            if extracted_type:
                reminder_type_alias = extracted_type

            message_raw = match_flexible_remind.group(2).strip()
            time_expression_raw = match_flexible_remind.group(
                3
            )  # Can be None if no preposition+time

            message = message_raw
            if time_expression_raw:
                time_expression_text = time_expression_raw.strip()

            # Clean up message from unwanted parts that might have been captured
            message = re.sub(
                r"^(i have a|i need to|remind me to)\s+", "", message, flags=re.IGNORECASE
            ).strip()

            # Heuristic to set type based on message content if not explicitly set
            if reminder_type_alias is None:
                if "birthday" in message:
                    reminder_type_alias = "birthday"
                elif (
                    "appointment" in message
                    or "meeting" in message
                    or "tournament" in message
                    or "dinner" in message
                ):
                    reminder_type_alias = "appointment"
                elif "task" in message or "todo" in message:
                    reminder_type_alias = "task"

            # If time expression was not found with preposition, try to find it elsewhere
            if not time_expression_text:
                # Look for simple "tomorrow", "today", "in X min/hours/days", etc.
                time_keywords_pattern = r"(tomorrow|today|in \d+\s*(?:min|hour|day)s?)"
                time_match_in_message = re.search(
                    time_keywords_pattern, message, flags=re.IGNORECASE
                )
                if time_match_in_message:
                    time_expression_text = time_match_in_message.group(0)
                    # Remove time part from message
                    message = message.replace(time_match_in_message.group(0), "").strip()

            if not time_expression_text:
                # TRY CONVERSATION HANDLER BEFORE FAILING
                conv_response = self._handle_conversation(command)
                if conv_response:
                    print(conv_response)
                    self._log_conversation("Agent", conv_response)
                    return

                response = "Could not find a clear time in your command. Please specify 'on', 'at', 'in', or 'by' with a time expression."
                print(response)
                self._log_conversation("Agent", response)
                return

            due_at = parse_time_expression(time_expression_text)

            if due_at:
                try:
                    if reminder_type_alias == "birthday":
                        reminder = self.manager.create_recurring_reminder(
                            message=f"BIRTHDAY: {message}",
                            start_date=due_at,
                            recurrence_type="yearly",
                            recurrence_details={"month": due_at.month, "day": due_at.day},
                        )
                        response = f"Birthday reminder set! ID: {reminder.id[:8]}..., Message: '{reminder.message}', Starts: {reminder.scheduled_time}"
                    elif reminder_type_alias in ["task", "appointment"]:
                        reminder = self.manager.create_one_time_reminder(
                            message=f"{reminder_type_alias.upper()}: {message}", due_at=due_at
                        )
                        response = f"{reminder_type_alias.capitalize()} reminder set! ID: {reminder.id[:8]}..., Message: '{reminder.message}', Due: {reminder.scheduled_time}"
                    else:  # Generic one-time reminder
                        reminder = self.manager.create_one_time_reminder(message, due_at)
                        response = f"Reminder set! ID: {reminder.id[:8]}..., Message: '{reminder.message}', Due: {reminder.scheduled_time}"
                except ValueError as e:
                    response = f"Error setting reminder: {e}"
                except TypeError as e:
                    response = f"Error setting reminder: {e}"
                print(response)
                self._log_conversation("Agent", response)
            else:
                response = (
                    "Could not understand the time for the reminder. Please be more specific."
                )
                print(response)
                self._log_conversation("Agent", response)
            return

        # Fallback to a simpler "remind me to..." if flexible parsing fails for creation
        match_simple_remind = re.match(r"remind me to (.+) (on|at|in|by) (.+)", command_lower)
        if match_simple_remind:
            message = match_simple_remind.group(1).strip()
            time_expression = (
                f"{match_simple_remind.group(2)} {match_simple_remind.group(3).strip()}"
            )
            due_at = parse_time_expression(time_expression)

            if due_at:
                try:
                    reminder = self.manager.create_one_time_reminder(message, due_at)
                    response = f"Reminder set! ID: {reminder.id[:8]}..., Message: '{reminder.message}', Due: {reminder.scheduled_time}"
                except ValueError as e:
                    response = f"Error setting reminder: {e}"
                except TypeError as e:
                    response = f"Error setting reminder: {e}"
                print(response)
                self._log_conversation("Agent", response)
            else:
                response = (
                    "Could not understand the time for the reminder. Please be more specific."
                )
                print(response)
                self._log_conversation("Agent", response)
            return

        # Generic recurring reminder (e.g., "set daily reminder for morning checkup")
        match_recurring = re.match(
            r"set (.+)\s+reminder(?: for)?\s+(.+?)\s+(daily|weekly|monthly|yearly)", command_lower
        )
        if match_recurring:
            reminder_type_str = match_recurring.group(3)
            message_content = match_recurring.group(2).strip()

            # Try to extract time from the message_content itself, or default
            start_date = parse_time_expression(message_content) or (
                datetime.now(timezone.utc) + timedelta(hours=1)
            )

            recurrence_details = None

            try:
                reminder = self.manager.create_recurring_reminder(
                    message_content, start_date, reminder_type_str, recurrence_details
                )
                response = f"Generic recurring reminder set! ID: {reminder.id[:8]}..., Message: '{reminder.message}', Type: {reminder.type.value}, Starts: {reminder.scheduled_time}"
            except ValueError as e:
                response = f"Error setting generic recurring reminder: {e}"
            except TypeError as e:
                response = f"Error setting generic recurring reminder: {e}"
            print(response)
            self._log_conversation("Agent", response)
            return

        # Check conversation handler as a last resort
        conv_response = self._handle_conversation(command)
        if conv_response:
            print(conv_response)
            self._log_conversation("Agent", conv_response)
            return

        response = "I didn't understand that command. Type 'help' for available commands."
        print(response)
        self._log_conversation("Agent", response)


if __name__ == "__main__":
    # Register a default CLI printer for alerts
    def cli_alert_printer(reminder: Reminder):
        print(
            f"\n\n!!! ALERT !!! Reminder: '{reminder.message}' is DUE NOW at {reminder.scheduled_time} (ID: {reminder.id[:8]}...)\nAgent> ",
            end="",
            flush=True,
        )

    agent = CLIAgent()
    agent.manager.register_notification_callback(cli_alert_printer)  # Register the CLI alert
    agent.run()
