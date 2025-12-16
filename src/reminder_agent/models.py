import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional


class ReminderType(Enum):
    ONE_TIME = "one-time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass
class Reminder:
    message: str
    scheduled_time: datetime
    type: ReminderType
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    recurrence_details: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.message:
            raise ValueError("Message cannot be empty.")
        if not isinstance(self.scheduled_time, datetime):
            raise TypeError("scheduled_time must be a datetime object.")
        if self.scheduled_time.tzinfo is None:
            raise ValueError("scheduled_time must be timezone-aware (UTC recommended).")
        if not isinstance(self.type, ReminderType):
            raise TypeError("type must be a ReminderType enum member.")

        # Basic validation for recurrence_details based on type
        if self.type not in [ReminderType.ONE_TIME, ReminderType.DAILY] and self.recurrence_details is None:
            raise ValueError(f"recurrence_details are required for {self.type.value} reminders.")
        
        # Further specific recurrence_details validation can be added here as needed
        # based on recurrence_type (e.g., days_of_week for weekly, day_of_month for monthly)
