# Quickstart Guide: Reminder Agent Basic Uses

This guide provides a quick overview of how to use the Reminder Agent Python library to manage one-time and recurring reminders.

## Installation (Conceptual)

Assuming the library is installed:

```bash
pip install reminder-agent-basic # Placeholder command
```

## Basic Usage

### 1. Initialize the ReminderManager

You'll need to instantiate the `ReminderManager`. For persistence, you'll need a persistence adapter (e.g., an in-memory adapter for testing, or a file-based one for actual use).

```python
from reminder_agent.core import ReminderManager
from reminder_agent.persistence import InMemoryPersistenceAdapter # Assuming this exists
from datetime import datetime, timedelta
import pytz # For timezone-aware datetimes

# Initialize with an in-memory persistence adapter for demonstration
persistence_adapter = InMemoryPersistenceAdapter()
manager = ReminderManager(persistence_adapter)
```

### 2. Create a One-Time Reminder

To create a reminder for a specific date and time:

```python
# Define a timezone-aware datetime (e.g., UTC)
# It's recommended to work with UTC internally and convert for display
utc_now = pytz.utc.localize(datetime.utcnow())
future_time = utc_now + timedelta(minutes=5) # 5 minutes from now

one_time_reminder = manager.create_one_time_reminder(
    message="Pick up groceries",
    due_at=future_time
)
print(f"Created one-time reminder: {one_time_reminder.message} due at {one_time_reminder.scheduled_time}")
```

### 3. Create a Recurring Reminder

To create a reminder that repeats (e.g., daily):

```python
utc_now = pytz.utc.localize(datetime.utcnow())
start_time = utc_now + timedelta(hours=1) # Start one hour from now

# Daily reminder
daily_reminder = manager.create_recurring_reminder(
    message="Daily Standup",
    start_date=start_time,
    recurrence_type="daily"
)
print(f"Created daily reminder: {daily_reminder.message} starting at {daily_reminder.scheduled_time}")

# Weekly reminder on specific days (e.g., Monday, Wednesday, Friday)
weekly_reminder = manager.create_recurring_reminder(
    message="Weekly Report",
    start_date=start_time,
    recurrence_type="weekly",
    recurrence_details={"days_of_week": ["Monday", "Wednesday", "Friday"]}
)
print(f"Created weekly reminder: {weekly_reminder.message}")

# Monthly reminder on a specific day of the month
monthly_reminder = manager.create_recurring_reminder(
    message="Pay Rent",
    start_date=start_time.replace(day=1), # Start on the 1st of the month
    recurrence_type="monthly",
    recurrence_details={"day_of_month": 1}
)
print(f"Created monthly reminder: {monthly_reminder.message}")
```

### 4. List Reminders

To view all active and pending reminders:

```python
all_reminders = manager.list_reminders()
print("\n--- All Pending Reminders ---")
for r in all_reminders:
    print(f"- ID: {r.id}, Message: {r.message}, Due: {r.scheduled_time}, Type: {r.type}")
```

### 5. Register a Notification Callback

To be notified when a reminder becomes due, register a callback function:

```python
def my_notification_handler(reminder):
    print(f"\n!!! REMINDER DUE !!! ID: {reminder.id}, Message: {reminder.message}")

manager.register_notification_callback(my_notification_handler)

# In a real application, you'd have a separate process or thread
# continuously checking for due reminders and triggering callbacks.
# The manager itself won't actively run a scheduler.
```

### 6. Delete a Reminder

To remove a reminder using its ID:

```python
# Assuming 'one_time_reminder' was created earlier
if 'one_time_reminder' in locals() and one_time_reminder:
    deleted = manager.delete_reminder(one_time_reminder.id)
    if deleted:
        print(f"\nDeleted reminder with ID: {one_time_reminder.id}")
    else:
        print(f"\nFailed to delete reminder with ID: {one_time_reminder.id}")

# Verify deletion
remaining_reminders = manager.list_reminders()
print("\n--- Reminders After Deletion ---")
for r in remaining_reminders:
    print(f"- ID: {r.id}, Message: {r.message}")
if not remaining_reminders:
    print("No reminders left.")
```
