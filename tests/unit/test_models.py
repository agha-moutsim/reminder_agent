import pytest
from datetime import datetime, timedelta, timezone
import uuid

from reminder_agent.models import Reminder, ReminderType


def test_reminder_creation_valid_one_time():
    """Test successful creation of a valid one-time reminder."""
    now_utc = datetime.now(timezone.utc)
    future_time = now_utc + timedelta(hours=1)
    reminder = Reminder(
        message="Buy groceries",
        scheduled_time=future_time,
        type=ReminderType.ONE_TIME
    )
    assert reminder.message == "Buy groceries"
    assert reminder.scheduled_time == future_time
    assert reminder.type == ReminderType.ONE_TIME
    assert reminder.recurrence_details is None
    assert isinstance(reminder.id, str)
    assert len(reminder.id) == 36  # UUID4 string length


def test_reminder_creation_valid_recurring():
    """Test successful creation of a valid recurring reminder."""
    now_utc = datetime.now(timezone.utc)
    future_time = now_utc + timedelta(hours=1)
    recurrence_details = {"days_of_week": ["Monday", "Wednesday"]}
    reminder = Reminder(
        message="Weekly meeting",
        scheduled_time=future_time,
        type=ReminderType.WEEKLY,
        recurrence_details=recurrence_details
    )
    assert reminder.message == "Weekly meeting"
    assert reminder.scheduled_time == future_time
    assert reminder.type == ReminderType.WEEKLY
    assert reminder.recurrence_details == recurrence_details


def test_reminder_message_empty_validation():
    """Test ValueError when message is empty."""
    now_utc = datetime.now(timezone.utc)
    future_time = now_utc + timedelta(hours=1)
    with pytest.raises(ValueError, match="Message cannot be empty."):
        Reminder(
            message="",
            scheduled_time=future_time,
            type=ReminderType.ONE_TIME
        )


def test_reminder_scheduled_time_type_validation():
    """Test TypeError when scheduled_time is not a datetime object."""
    with pytest.raises(TypeError, match="scheduled_time must be a datetime object."):
        Reminder(
            message="Valid message",
            scheduled_time="not a datetime",
            type=ReminderType.ONE_TIME
        )


def test_reminder_scheduled_time_timezone_validation():
    """Test ValueError when scheduled_time is not timezone-aware."""
    naive_time = datetime.now()
    with pytest.raises(ValueError, match="scheduled_time must be timezone-aware"):
        Reminder(
            message="Valid message",
            scheduled_time=naive_time,
            type=ReminderType.ONE_TIME
        )


def test_reminder_type_enum_validation():
    """Test TypeError when type is not a ReminderType enum member."""
    now_utc = datetime.now(timezone.utc)
    future_time = now_utc + timedelta(hours=1)
    with pytest.raises(TypeError, match="type must be a ReminderType enum member."):
        Reminder(
            message="Valid message",
            scheduled_time=future_time,
            type="invalid_type"  # type: ignore
        )


def test_reminder_recurrence_details_missing_for_recurring():
    """Test ValueError when recurrence_details are missing for recurring reminders."""
    now_utc = datetime.now(timezone.utc)
    future_time = now_utc + timedelta(hours=1)
    with pytest.raises(ValueError, match="recurrence_details are required for weekly reminders."):
        Reminder(
            message="Weekly standup",
            scheduled_time=future_time,
            type=ReminderType.WEEKLY,
            recurrence_details=None
        )


def test_reminder_id_generation():
    """Test that a unique ID is generated if not provided."""
    now_utc = datetime.now(timezone.utc)
    future_time = now_utc + timedelta(hours=1)
    reminder1 = Reminder(
        message="Task 1",
        scheduled_time=future_time,
        type=ReminderType.ONE_TIME
    )
    reminder2 = Reminder(
        message="Task 2",
        scheduled_time=future_time,
        type=ReminderType.ONE_TIME
    )
    assert reminder1.id != reminder2.id
    assert isinstance(uuid.UUID(reminder1.id), uuid.UUID) # Test if it's a valid UUID
