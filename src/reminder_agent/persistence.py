from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from reminder_agent.models import Reminder


class PersistenceAdapter(ABC):
    """
    Abstract Base Class for persistence adapters.
    Defines the interface for storing and retrieving Reminder objects.
    """

    @abstractmethod
    def save_reminder(self, reminder: Reminder) -> None:
        """
        Saves a single reminder. If a reminder with the same ID already exists,
        it should be updated.
        """
        pass

    @abstractmethod
    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        """
        Retrieves a reminder by its ID.
        Returns None if no reminder with the given ID is found.
        """
        pass

    @abstractmethod
    def get_all_reminders(self) -> List[Reminder]:
        """
        Retrieves all stored reminders.
        """
        pass

    @abstractmethod
    def delete_reminder(self, reminder_id: str) -> bool:
        """
        Deletes a reminder by its ID.
        Returns True if the reminder was deleted, False if not found.
        """
        pass


class InMemoryPersistenceAdapter(PersistenceAdapter):
    """
    An in-memory implementation of the PersistenceAdapter for testing and basic use.
    Reminders are stored in a dictionary and are not persisted across application runs.
    """

    def __init__(self):
        self._reminders: Dict[str, Reminder] = {}

    def save_reminder(self, reminder: Reminder) -> None:
        self._reminders[reminder.id] = reminder

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        return self._reminders.get(reminder_id)

    def get_all_reminders(self) -> List[Reminder]:
        return list(self._reminders.values())

    def delete_reminder(self, reminder_id: str) -> bool:
        if reminder_id in self._reminders:
            del self._reminders[reminder_id]
            return True
        return False
