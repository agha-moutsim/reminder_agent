import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from reminder_agent.core import ReminderManager # This might fail initially
from reminder_agent.persistence import InMemoryPersistenceAdapter
from reminder_agent.models import Reminder, ReminderType
from reminder_agent.callbacks import NotificationCallbackManager # This will fail initially


@pytest.fixture
def reminder_manager():
    return ReminderManager(InMemoryPersistenceAdapter())


@pytest.fixture
def mock_callback():
    """A mock callback function for testing."""
    return Mock()


# T034: Implement test case for register_notification_callback
def test_register_notification_callback(reminder_manager, mock_callback):
    # _callback_manager is not defined yet, this test is expected to fail initially.
    # We will assume a _callback_manager attribute and methods like has_callbacks, _callbacks, trigger_callbacks exist.
    # These will be implemented in T037 and T038/T039.
    assert not reminder_manager._callback_manager.has_callbacks()
    reminder_manager.register_notification_callback(mock_callback)
    assert reminder_manager._callback_manager.has_callbacks()
    assert mock_callback in reminder_manager._callback_manager._callbacks


# T035: Implement test case for unregister_notification_callback
def test_unregister_notification_callback(reminder_manager, mock_callback):
    reminder_manager.register_notification_callback(mock_callback)
    assert reminder_manager._callback_manager.has_callbacks()

    reminder_manager.unregister_notification_callback(mock_callback)
    assert not reminder_manager._callback_manager.has_callbacks()
    assert mock_callback not in reminder_manager._callback_manager._callbacks


# T036: Implement test case for triggering registered callbacks when a reminder is due
def test_trigger_callbacks_on_due_reminder(reminder_manager, mock_callback):
    reminder_manager.register_notification_callback(mock_callback)
    
    message = "Time for coffee"
    due_at = datetime.now(timezone.utc) + timedelta(seconds=1) # A reminder due very soon
    reminder = reminder_manager.create_one_time_reminder(message, due_at)

    # In a real scenario, a scheduler would trigger this. For testing, we simulate.
    # This assumes a method like _check_and_trigger_due_reminders exists in ReminderManager
    # which is not yet implemented.
    # We will need to mock out the persistence adapter to control due reminders.

    # Temporarily, we will directly call the trigger method (which will be in ReminderManager later)
    # This will fail until the _callback_manager and trigger logic is in place.
    reminder_manager._callback_manager.trigger_callbacks(reminder)
    mock_callback.assert_called_once_with(reminder)
