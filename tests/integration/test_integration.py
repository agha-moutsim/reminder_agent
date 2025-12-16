import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from reminder_agent.core import ReminderManager
from reminder_agent.persistence import InMemoryPersistenceAdapter
from reminder_agent.models import Reminder, ReminderType


@pytest.fixture
def manager():
    """Provides a ReminderManager with an InMemoryPersistenceAdapter."""
    return ReminderManager(InMemoryPersistenceAdapter())


def test_e2e_create_list_delete_one_time_reminder(manager):
    """
    End-to-end test for creating, listing, and deleting a one-time reminder.
    """
    # 1. Create a reminder
    message = "Integration Test Reminder"
    due_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    created_reminder = manager.create_one_time_reminder(message, due_at)

    assert created_reminder is not None
    assert created_reminder.message == message
    assert created_reminder.scheduled_time == due_at
    assert created_reminder.type == ReminderType.ONE_TIME

    # 2. List reminders and verify the created one is present
    all_reminders = manager.list_reminders()
    assert len(all_reminders) == 1
    assert created_reminder in all_reminders

    # 3. Delete the reminder
    deleted = manager.delete_reminder(created_reminder.id)
    assert deleted is True

    # 4. List reminders again and verify it's gone
    remaining_reminders = manager.list_reminders()
    assert len(remaining_reminders) == 0


def test_e2e_create_list_recurring_reminder(manager):
    """
    End-to-end test for creating and listing a recurring reminder.
    """
    message = "Recurring Integration Test"
    start_date = datetime.now(timezone.utc) + timedelta(days=1)
    recurrence_details = {"days_of_week": ["Monday"]}

    created_reminder = manager.create_recurring_reminder(
        message, start_date, "weekly", recurrence_details
    )

    assert created_reminder is not None
    assert created_reminder.message == message
    assert created_reminder.scheduled_time == start_date
    assert created_reminder.type == ReminderType.WEEKLY
    assert created_reminder.recurrence_details == recurrence_details

    # List reminders and verify the created one is present
    all_reminders = manager.list_reminders()
    assert len(all_reminders) == 1
    assert created_reminder in all_reminders


def test_e2e_callback_triggering(manager):
    """
    End-to-end test for registering and triggering callbacks.
    """
    mock_handler = Mock()
    manager.register_notification_callback(mock_handler)

    message = "Callback Test Reminder"
    # Create a reminder in the very near future
    due_at = datetime.now(timezone.utc) + timedelta(seconds=2) 
    created_reminder = manager.create_one_time_reminder(message, due_at)

    # Manually trigger the callback. In a real system, a scheduler would do this.
    manager._callback_manager.trigger_callbacks(created_reminder)

    mock_handler.assert_called_once_with(created_reminder)

    manager.unregister_notification_callback(mock_handler)
    assert not manager._callback_manager.has_callbacks()
