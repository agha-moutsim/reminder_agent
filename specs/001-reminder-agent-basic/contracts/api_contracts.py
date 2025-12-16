# contracts/api_contracts.py

from datetime import datetime
from typing import List, Callable, Dict, Any, Optional
import uuid

# Define Reminder type (conceptual, would be a dataclass in models.py)
class Reminder:
    id: str
    message: str
    scheduled_time: datetime # UTC
    type: str # "one-time", "daily", "weekly", "monthly", "yearly"
    recurrence_details: Optional[Dict[str, Any]] = None

class ReminderManager:
    """
    Manages the creation, listing, and deletion of reminders.
    """

    def __init__(self, persistence_adapter: Any):
        """
        Initializes the ReminderManager with a persistence adapter.
        """
        pass

    def create_one_time_reminder(self, message: str, due_at: datetime) -> Reminder:
        """
        Creates a new one-time reminder.

        Args:
            message: The message content of the reminder.
            due_at: The exact UTC datetime when the reminder should become due.

        Returns:
            The created Reminder object.

        Raises:
            ValueError: If due_at is in the past.
        """
        pass

    def create_recurring_reminder(
        self,
        message: str,
        start_date: datetime,
        recurrence_type: str, # "daily", "weekly", "monthly", "yearly"
        recurrence_details: Optional[Dict[str, Any]] = None
    ) -> Reminder:
        """
        Creates a new recurring reminder.

        Args:
            message: The message content of the reminder.
            start_date: The UTC datetime when the recurrence pattern should start.
            recurrence_type: The type of recurrence (e.g., "daily", "weekly").
            recurrence_details: A dictionary containing details specific to the recurrence type.

        Returns:
            The created Reminder object.

        Raises:
            ValueError: If recurrence_type is invalid or recurrence_details are malformed.
        """
        pass

    def list_reminders(self, include_past: bool = False) -> List[Reminder]:
        """
        Lists all active/pending reminders.

        Args:
            include_past: If True, includes reminders that are due in the past.

        Returns:
            A list of Reminder objects.
        """
        pass

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        """
        Retrieves a single reminder by its ID.

        Args:
            reminder_id: The unique identifier of the reminder.

        Returns:
            The Reminder object if found, otherwise None.
        """
        pass


    def delete_reminder(self, reminder_id: str) -> bool:
        """
        Deletes a reminder by its unique ID.

        Args:
            reminder_id: The unique identifier of the reminder to delete.

        Returns:
            True if the reminder was successfully deleted, False otherwise.
        """
        pass

    def register_notification_callback(self, callback: Callable[[Reminder], None]):
        """
        Registers a callback function to be executed when a reminder becomes due.

        Args:
            callback: A callable that accepts a Reminder object as an argument.
        """
        pass

    def unregister_notification_callback(self, callback: Callable[[Reminder], None]):
        """
        Unregisters a previously registered callback function.

        Args:
            callback: The callback function to unregister.
        """
        pass
