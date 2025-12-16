# Data Model: Reminder Agent Basic Uses

## Entity: Reminder

**Description**: Represents a scheduled notification that can be one-time or recurring.

**Attributes**:

*   `id`:
    *   **Type**: String (UUID or similar unique identifier)
    *   **Description**: A unique identifier for the reminder.
    *   **Validation**: Must be a non-empty string.
    *   **Uniqueness**: Primary key.
*   `message`:
    *   **Type**: String
    *   **Description**: The textual content of the reminder.
    *   **Validation**: Must be a non-empty string.
*   `scheduled_time`:
    *   **Type**: Datetime object (UTC)
    *   **Description**: The precise time (date and time) when the reminder is initially scheduled to become due or when its recurrence pattern starts. Stored in UTC to avoid timezone issues.
    *   **Validation**: Must be a valid future datetime for one-time reminders.
*   `type`:
    *   **Type**: Enum (String: "one-time", "daily", "weekly", "monthly", "yearly")
    *   **Description**: Defines the recurrence pattern of the reminder.
    *   **Validation**: Must be one of the specified enum values.
*   `recurrence_details`:
    *   **Type**: Dictionary/Object (Optional)
    *   **Description**: Stores additional details specific to recurring reminders.
        *   For "weekly": e.g., `{"days_of_week": ["Monday", "Wednesday"]}`
        *   For "monthly": e.g., `{"day_of_month": 15}`
        *   For "yearly": e.g., `{"month": 12, "day": 25}`
    *   **Validation**: Structure depends on `type`. Must be valid for the chosen recurrence type.

**Relationships**:

*   None (Reminder is a standalone entity in this basic model).

**Validation Rules**:

*   For `type == "one-time"`, `scheduled_time` MUST be in the future relative to the time of creation.
*   `message` MUST NOT be empty.
*   `id` MUST be unique.
*   `recurrence_details` MUST be consistent with `type` (e.g., if `type` is "monthly", `recurrence_details` must contain `day_of_month`).

**State Transitions**:

*   **Created**: Initial state after a reminder is set.
*   **Pending**: Active and awaiting its scheduled time.
*   **Due**: When `scheduled_time` is reached (triggers notification callback).
*   **Deleted**: Permanently removed from the system.

**Open Questions/Considerations**:

*   How are multiple occurrences of a recurring reminder represented? (e.g., each occurrence as a separate instance or a single reminder generating future instances on demand).
*   Handling of reminder modification (e.g., changing message, time, or recurrence). (Out of scope for basic uses, but noted for future).
