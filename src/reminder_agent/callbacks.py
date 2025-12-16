from typing import Callable, List
from reminder_agent.models import Reminder


class NotificationCallbackManager:
    """
    Manages registration and triggering of notification callbacks.
    """
    def __init__(self):
        self._callbacks: List[Callable[[Reminder], None]] = []

    def register_callback(self, callback: Callable[[Reminder], None]) -> None:
        """Registers a callback function."""
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[Reminder], None]) -> None:
        """Unregisters a callback function."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def trigger_callbacks(self, reminder: Reminder) -> None:
        """Triggers all registered callbacks with the given reminder."""
        for callback in self._callbacks:
            try:
                callback(reminder)
            except Exception as e:
                # Log the error but don't stop other callbacks
                print(f"Error in callback {callback.__name__}: {e}")

    def has_callbacks(self) -> bool:
        """Checks if there are any registered callbacks."""
        return bool(self._callbacks)
