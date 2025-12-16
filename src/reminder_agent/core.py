from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any, Callable

from reminder_agent.models import Reminder, ReminderType
from reminder_agent.persistence import PersistenceAdapter
from reminder_agent.callbacks import NotificationCallbackManager


class ReminderManager:
    """
    Manages the creation, listing, and deletion of reminders.
    """

    def __init__(self, persistence_adapter: PersistenceAdapter):
        """
        Initializes the ReminderManager with a persistence adapter.
        """
        self._persistence_adapter = persistence_adapter
        self._callback_manager = NotificationCallbackManager()

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
        if due_at < datetime.now(timezone.utc):
            raise ValueError("due_at must be in the future.")
        
        # Ensure scheduled_time is timezone-aware
        if due_at.tzinfo is None:
            raise ValueError("due_at must be timezone-aware (UTC recommended).")

        reminder = Reminder(
            message=message,
            scheduled_time=due_at,
            type=ReminderType.ONE_TIME
        )
        self._persistence_adapter.save_reminder(reminder)
        return reminder

    def create_recurring_reminder(
        self,
        message: str,
        start_date: datetime,
        recurrence_type: str,
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
        try:
            reminder_type = ReminderType(recurrence_type)
        except ValueError:
            raise ValueError(f"Invalid recurrence_type: {recurrence_type}. Must be one of {[rt.value for rt in ReminderType if rt != ReminderType.ONE_TIME]}")

        # Basic validation for recurrence_details based on type (more specific validation is in Reminder.__post_init__)
        if reminder_type not in [ReminderType.ONE_TIME, ReminderType.DAILY] and recurrence_details is None:
            raise ValueError(f"recurrence_details are required for {reminder_type.value} reminders.")

        # Ensure start_date is timezone-aware
        if start_date.tzinfo is None:
            raise ValueError("start_date must be timezone-aware (UTC recommended).")

        reminder = Reminder(
            message=message,
            scheduled_time=start_date,
            type=reminder_type,
            recurrence_details=recurrence_details
        )
        self._persistence_adapter.save_reminder(reminder)
        return reminder


    def list_reminders(self, include_past: bool = False) -> List[Reminder]:
        """
        Lists all active/pending reminders.

        Args:
            include_past: If True, includes reminders that are due in the past.

        Returns:
            A list of Reminder objects.
        """
        all_reminders = self._persistence_adapter.get_all_reminders()
        if include_past:
            return all_reminders
        
        now_utc = datetime.now(timezone.utc)
        return [r for r in all_reminders if r.scheduled_time > now_utc]

    def delete_reminder(self, reminder_id: str) -> bool:
        """
        Deletes a reminder by its unique ID.

        Args:
            reminder_id: The unique identifier of the reminder to delete.

        Returns:
            True if the reminder was successfully deleted, False otherwise.
        """
        return self._persistence_adapter.delete_reminder(reminder_id)

    def register_notification_callback(self, callback: Callable[[Reminder], None]):
        """
        Registers a callback function to be executed when a reminder becomes due.

        Args:
            callback: A callable that accepts a Reminder object as an argument.
        """
        self._callback_manager.register_callback(callback)

    def unregister_notification_callback(self, callback: Callable[[Reminder], None]):
        """
        Unregisters a previously registered callback function.

        Args:
            callback: The callback function to unregister.
        """
        self._callback_manager.unregister_callback(callback)

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        """
        Retrieves a single reminder by its ID.

        Args:
            reminder_id: The unique identifier of the reminder.

        Returns:
            The Reminder object if found, otherwise None.
        """
        return self._persistence_adapter.get_reminder(reminder_id)
