import pytest
from datetime import datetime, timedelta, timezone
from typing import Type

from reminder_agent.models import Reminder, ReminderType
from reminder_agent.persistence import PersistenceAdapter, InMemoryPersistenceAdapter


@pytest.fixture
def sample_reminder():
    """Fixture to provide a sample Reminder object."""
    now_utc = datetime.now(timezone.utc)
    future_time = now_utc + timedelta(hours=1)
    return Reminder(
        message="Test Reminder",
        scheduled_time=future_time,
        type=ReminderType.ONE_TIME
    )


@pytest.fixture(params=[InMemoryPersistenceAdapter])
def persistence_adapter(request) -> PersistenceAdapter:
    """Fixture to provide different persistence adapter implementations."""
    return request.param()


def test_save_and_get_reminder(persistence_adapter: PersistenceAdapter, sample_reminder: Reminder):
    """Test saving a reminder and then retrieving it."""
    persistence_adapter.save_reminder(sample_reminder)
    retrieved_reminder = persistence_adapter.get_reminder(sample_reminder.id)
    assert retrieved_reminder == sample_reminder


def test_get_non_existent_reminder(persistence_adapter: PersistenceAdapter):
    """Test retrieving a reminder that does not exist."""
    assert persistence_adapter.get_reminder("non-existent-id") is None


def test_get_all_reminders_empty(persistence_adapter: PersistenceAdapter):
    """Test retrieving all reminders when none are present."""
    assert persistence_adapter.get_all_reminders() == []


def test_get_all_reminders_multiple(persistence_adapter: PersistenceAdapter):
    """Test retrieving all reminders when multiple are present."""
    now_utc = datetime.now(timezone.utc)
    reminder1 = Reminder(message="R1", scheduled_time=now_utc + timedelta(hours=1), type=ReminderType.ONE_TIME)
    reminder2 = Reminder(message="R2", scheduled_time=now_utc + timedelta(hours=2), type=ReminderType.ONE_TIME)
    
    persistence_adapter.save_reminder(reminder1)
    persistence_adapter.save_reminder(reminder2)

    all_reminders = persistence_adapter.get_all_reminders()
    assert len(all_reminders) == 2
    assert reminder1 in all_reminders
    assert reminder2 in all_reminders


def test_delete_reminder_success(persistence_adapter: PersistenceAdapter, sample_reminder: Reminder):
    """Test successful deletion of an existing reminder."""
    persistence_adapter.save_reminder(sample_reminder)
    assert persistence_adapter.delete_reminder(sample_reminder.id) is True
    assert persistence_adapter.get_reminder(sample_reminder.id) is None


def test_delete_reminder_non_existent(persistence_adapter: PersistenceAdapter):
    """Test deleting a reminder that does not exist."""
    assert persistence_adapter.delete_reminder("non-existent-id") is False


def test_save_updates_reminder(persistence_adapter: PersistenceAdapter, sample_reminder: Reminder):
    """Test that saving a reminder with an existing ID updates it."""
    persistence_adapter.save_reminder(sample_reminder)
    
    updated_message = "Updated Test Reminder"
    updated_reminder = Reminder(
        id=sample_reminder.id,
        message=updated_message,
        scheduled_time=sample_reminder.scheduled_time,
        type=sample_reminder.type
    )
    persistence_adapter.save_reminder(updated_reminder)
    
    retrieved_reminder = persistence_adapter.get_reminder(sample_reminder.id)
    assert retrieved_reminder.message == updated_message
    assert retrieved_reminder.id == sample_reminder.id
    assert len(persistence_adapter.get_all_reminders()) == 1 # Should still be only one reminder
