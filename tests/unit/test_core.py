import pytest
from datetime import datetime, timedelta, timezone

from reminder_agent.core import ReminderManager
from reminder_agent.persistence import InMemoryPersistenceAdapter
from reminder_agent.models import Reminder, ReminderType


# Fixture for a ReminderManager with InMemoryPersistenceAdapter
@pytest.fixture
def reminder_manager():
    return ReminderManager(InMemoryPersistenceAdapter())


# T012: Implement test case for valid one-time reminder creation
def test_create_one_time_reminder_success(reminder_manager):
    message = "Buy milk"
    due_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    reminder = reminder_manager.create_one_time_reminder(message, due_at)

    assert isinstance(reminder, Reminder)
    assert reminder.message == message
    assert reminder.scheduled_time == due_at
    assert reminder.type == ReminderType.ONE_TIME
    assert reminder.id is not None
    assert reminder.recurrence_details is None

    # Verify it's stored
    retrieved_reminder = reminder_manager.get_reminder(reminder.id)
    assert retrieved_reminder == reminder


# T013: Implement test case for ValueError when due_at is in the past
def test_create_one_time_reminder_past_due_at_fails(reminder_manager):
    message = "Expired reminder"
    past_time = datetime.now(timezone.utc) - timedelta(minutes=30)
    with pytest.raises(ValueError, match="due_at must be in the future."):
        reminder_manager.create_one_time_reminder(message, past_time)


# T019: Implement test case for listing multiple reminders
def test_list_reminders_multiple(reminder_manager):
    now_utc = datetime.now(timezone.utc)
    reminder1 = reminder_manager.create_one_time_reminder("Task 1", now_utc + timedelta(hours=1))
    reminder2 = reminder_manager.create_one_time_reminder("Task 2", now_utc + timedelta(hours=2))

    reminders = reminder_manager.list_reminders()

    assert len(reminders) == 2
    assert reminder1 in reminders
    assert reminder2 in reminders


# T020: Implement test case for an empty list of reminders
def test_list_reminders_empty(reminder_manager):
    reminders = reminder_manager.list_reminders()
    assert len(reminders) == 0
    assert reminders == []


# T023: Implement test case for successful deletion by ID
def test_delete_reminder_success(reminder_manager):
    message = "Reminder to delete"
    due_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    reminder = reminder_manager.create_one_time_reminder(message, due_at)
    
    assert reminder_manager.get_reminder(reminder.id) is not None
    assert reminder_manager.delete_reminder(reminder.id) is True
    assert reminder_manager.get_reminder(reminder.id) is None
    assert reminder_manager.list_reminders() == []


# T024: Implement test case for deleting a non-existent reminder
def test_delete_reminder_non_existent(reminder_manager):
    assert reminder_manager.delete_reminder("non-existent-id") is False
    assert reminder_manager.list_reminders() == []


# T027: Implement test case for "daily" recurrence
def test_create_recurring_reminder_daily(reminder_manager):
    message = "Daily standup"
    start_date = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    # create_recurring_reminder not implemented yet
    reminder = reminder_manager.create_recurring_reminder(message, start_date, "daily")

    assert isinstance(reminder, Reminder)
    assert reminder.message == message
    assert reminder.scheduled_time == start_date
    assert reminder.type == ReminderType.DAILY
    assert reminder.id is not None
    assert reminder.recurrence_details is None


# T028: Implement test case for "weekly" recurrence
def test_create_recurring_reminder_weekly(reminder_manager):
    message = "Weekly report"
    start_date = datetime.now(timezone.utc) + timedelta(minutes=10)
    recurrence_details = {"days_of_week": ["Monday", "Wednesday"]}

    reminder = reminder_manager.create_recurring_reminder(message, start_date, "weekly", recurrence_details)

    assert isinstance(reminder, Reminder)
    assert reminder.message == message
    assert reminder.scheduled_time == start_date
    assert reminder.type == ReminderType.WEEKLY
    assert reminder.id is not None
    assert reminder.recurrence_details == recurrence_details


# T029: Implement test case for "monthly" recurrence
def test_create_recurring_reminder_monthly(reminder_manager):
    message = "Pay rent"
    start_date = datetime.now(timezone.utc) + timedelta(days=5) # Example: next 5 days
    recurrence_details = {"day_of_month": start_date.day}

    reminder = reminder_manager.create_recurring_reminder(message, start_date, "monthly", recurrence_details)

    assert isinstance(reminder, Reminder)
    assert reminder.message == message
    assert reminder.scheduled_time == start_date
    assert reminder.type == ReminderType.MONTHLY
    assert reminder.id is not None
    assert reminder.recurrence_details == recurrence_details


# T030: Implement test case for "yearly" recurrence
def test_create_recurring_reminder_yearly(reminder_manager):
    message = "Birthday"
    start_date = datetime.now(timezone.utc).replace(month=12, day=25, hour=9, minute=0, second=0, microsecond=0) + timedelta(days=365) # Next Christmas
    recurrence_details = {"month": start_date.month, "day": start_date.day}

    reminder = reminder_manager.create_recurring_reminder(message, start_date, "yearly", recurrence_details)

    assert isinstance(reminder, Reminder)
    assert reminder.message == message
    assert reminder.scheduled_time == start_date
    assert reminder.type == ReminderType.YEARLY
    assert reminder.id is not None
    assert reminder.recurrence_details == recurrence_details


# T031: Implement test cases for invalid recurrence_type or recurrence_details
def test_create_recurring_reminder_invalid_type_fails(reminder_manager):
    message = "Invalid reminder"
    start_date = datetime.now(timezone.utc) + timedelta(minutes=10)
    with pytest.raises(ValueError, match="Invalid recurrence_type"):
        reminder_manager.create_recurring_reminder(message, start_date, "invalid")


def test_create_recurring_reminder_missing_details_fails(reminder_manager):
    message = "Invalid reminder"
    start_date = datetime.now(timezone.utc) + timedelta(minutes=10)
    with pytest.raises(ValueError, match="recurrence_details are required for weekly reminders."):
        reminder_manager.create_recurring_reminder(message, start_date, "weekly", recurrence_details=None)