import time
from datetime import datetime, timedelta, timezone
import pytz

from reminder_agent.core import ReminderManager
from reminder_agent.persistence import InMemoryPersistenceAdapter
from reminder_agent.models import Reminder, ReminderType


def main():
    print("--- Demonstrating Reminder Agent ---")

    # 1. Initialize the ReminderManager
    persistence_adapter = InMemoryPersistenceAdapter()
    manager = ReminderManager(persistence_adapter)
    print("\nInitialized ReminderManager with InMemoryPersistenceAdapter.")

    # 2. Create a One-Time Reminder
    utc_now = datetime.now(timezone.utc)
    future_time_one_time = utc_now + timedelta(seconds=5) # 5 seconds from now
    one_time_reminder = manager.create_one_time_reminder(
        message="Pick up groceries",
        due_at=future_time_one_time
    )
    print(f"\nCreated one-time reminder: '{one_time_reminder.message}' due at {one_time_reminder.scheduled_time} (ID: {one_time_reminder.id[:8]}...)")

    # 3. Create a Recurring Reminder (Daily)
    future_time_recurring = utc_now + timedelta(seconds=10) # 10 seconds from now
    daily_reminder = manager.create_recurring_reminder(
        message="Daily Standup",
        start_date=future_time_recurring,
        recurrence_type="daily"
    )
    print(f"Created daily recurring reminder: '{daily_reminder.message}' starting at {daily_reminder.scheduled_time} (ID: {daily_reminder.id[:8]}...)")

    # 4. List Reminders
    print("\n--- Listing all current reminders ---")
    reminders_before_delete = manager.list_reminders()
    if reminders_before_delete:
        for r in reminders_before_delete:
            print(f"- ID: {r.id[:8]}..., Message: '{r.message}', Due: {r.scheduled_time}, Type: {r.type.value}")
    else:
        print("No reminders found.")

    # 5. Register a Notification Callback
    def my_notification_handler(reminder: Reminder):
        print(f"\n!!! REMINDER DUE !!! [Callback Triggered] ID: {reminder.id[:8]}..., Message: '{reminder.message}'")

    manager.register_notification_callback(my_notification_handler)
    print("\nRegistered a notification callback.")

    print("\n--- Waiting for reminders to become due... ---")
    # Simulate a simple check for due reminders and trigger callbacks
    # In a real application, this would be a background scheduler.
    
    # We'll wait a bit for the one-time reminder to pass its due time
    time.sleep(6) # Wait 6 seconds (one-time reminder due in 5s)
    
    # Manually check and trigger for the one-time reminder
    due_reminders = [
        r for r in manager.list_reminders(include_past=True) 
        if r.scheduled_time <= datetime.now(timezone.utc) and r.type == ReminderType.ONE_TIME
    ]
    for r in due_reminders:
        manager._callback_manager.trigger_callbacks(r)
        # For one-time reminders, delete them after triggering
        manager.delete_reminder(r.id)
    
    # Manually check and trigger for the daily reminder (if its time has passed)
    # Note: For recurring reminders, a real scheduler would calculate the next occurrence
    # and re-save the reminder with the updated scheduled_time.
    # For this demo, we're just demonstrating the initial trigger for its 'start_date'.
    due_reminders_daily = [
        r for r in manager.list_reminders(include_past=True) 
        if r.scheduled_time <= datetime.now(timezone.utc) and r.type == ReminderType.DAILY
    ]
    for r in due_reminders_daily:
        manager._callback_manager.trigger_callbacks(r)
        # For recurring reminders, we might update their next due time or leave them
        # For this simple demo, we'll just demonstrate the trigger.

    print("\n--- Listing reminders after simulated due checks ---")
    reminders_after_check = manager.list_reminders()
    if reminders_after_check:
        for r in reminders_after_check:
            print(f"- ID: {r.id[:8]}..., Message: '{r.message}', Due: {r.scheduled_time}, Type: {r.type.value}")
    else:
        print("No active reminders left.")
    
    # 6. Delete a Reminder
    if daily_reminder.id:
        print(f"\n--- Deleting the daily recurring reminder (ID: {daily_reminder.id[:8]}...) ---")
        deleted = manager.delete_reminder(daily_reminder.id)
        if deleted:
            print("Daily recurring reminder deleted successfully.")
        else:
            print("Failed to delete daily recurring reminder.")

    print("\n--- Final list of reminders ---")
    final_reminders = manager.list_reminders()
    if final_reminders:
        for r in final_reminders:
            print(f"- ID: {r.id[:8]}..., Message: '{r.message}', Due: {r.scheduled_time}, Type: {r.type.value}")
    else:
        print("No reminders left.")

    print("\n--- Reminder Agent Demo Complete ---")


if __name__ == "__main__":
    main()
