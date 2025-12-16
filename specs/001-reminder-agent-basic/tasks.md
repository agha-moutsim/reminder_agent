## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

-   [ ] T001 Initialize Python project with `uv init` and configure for `src/reminder_agent` (creates `pyproject.toml`)
-   [ ] T002 Create remaining project directories: `src/reminder_agent/`, `tests/unit/`, `tests/integration/`
-   [ ] T003 Initialize `src/reminder_agent/__init__.py`
-   [ ] T004 Configure linting (`ruff`) and formatting (`black`) tools in `pyproject.toml` (add `ruff` and `black` as dev dependencies, and update `pyproject.toml` configuration)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented. This includes the `Reminder` model and the persistence interface.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

-   [ ] T005 [P] Create `src/reminder_agent/models.py` for Reminder dataclass
-   [ ] T006 [P] Create `tests/unit/test_models.py` for `Reminder` dataclass validation (e.g., id, message non-empty)
-   [ ] T007 Implement `Reminder` dataclass in `src/reminder_agent/models.py` as defined in `data-model.md`
-   [ ] T008 [P] Create `src/reminder_agent/persistence.py` for `PersistenceAdapter` interface (ABC)
-   [ ] T009 [P] Create `tests/unit/test_persistence.py` for `PersistenceAdapter` interface
-   [ ] T010 Implement `PersistenceAdapter` ABC and a basic `InMemoryPersistenceAdapter` in `src/reminder_agent/persistence.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Set a One-Time Reminder (Priority: P1) 🎯 MVP

**Goal**: Allow users to successfully create and store one-time reminders.

**Independent Test**: Successfully create a one-time reminder and verify its attributes by retrieving it from persistence.

### Tests for User Story 1 ⚠️
> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

-   [ ] T011 [P] [US1] Create `tests/unit/test_core.py` for `create_one_time_reminder`
-   [ ] T012 [US1] Implement test case for valid one-time reminder creation in `tests/unit/test_core.py`
-   [ ] T013 [US1] Implement test case for `ValueError` when `due_at` is in the past in `tests/unit/test_core.py`

### Implementation for User Story 1

-   [ ] T014 [P] [US1] Create `src/reminder_agent/core.py` for `ReminderManager` class
-   [ ] T015 [US1] Implement `ReminderManager.__init__` to accept `PersistenceAdapter` in `src/reminder_agent/core.py`
-   [ ] T016 [US1] Implement `create_one_time_reminder` in `src/reminder_agent/core.py`
-   [ ] T017 [US1] Ensure `create_one_time_reminder` validates `due_at` is in the future.

**Checkpoint**: User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - List All Pending Reminders (Priority: P1)

**Goal**: Allow users to view all active and pending reminders.

**Independent Test**: Create multiple reminders, then retrieve and verify the list of reminders.

### Tests for User Story 2 ⚠️

-   [ ] T018 [P] [US2] Add test cases for `list_reminders` in `tests/unit/test_core.py`
-   [ ] T019 [US2] Implement test case for listing multiple reminders in `tests/unit/test_core.py`
-   [ ] T020 [US2] Implement test case for an empty list of reminders in `tests/unit/test_core.py`

### Implementation for User Story 2

-   [ ] T021 [US2] Implement `list_reminders` in `src/reminder_agent/core.py`

**Checkpoint**: User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Delete a Reminder (Priority: P2)

**Goal**: Allow users to remove unwanted reminders.

**Independent Test**: Create a reminder, delete it, and then verify its absence from the list.

### Tests for User Story 3 ⚠️

-   [ ] T022 [P] [US3] Add test cases for `delete_reminder` in `tests/unit/test_core.py`
-   [ ] T023 [US3] Implement test case for successful deletion by ID in `tests/unit/test_core.py`
-   [ ] T024 [US3] Implement test case for deleting a non-existent reminder in `tests/unit/test_core.py`

### Implementation for User Story 3

-   [ ] T025 [US3] Implement `delete_reminder` in `src/reminder_agent/core.py`

**Checkpoint**: All user stories implemented so far should be independently functional.

---

### Phase 6: Create Recurring Reminders

**Goal**: Allow users to create reminders with various recurrence patterns.

**Independent Test**: Create a recurring reminder and verify its attributes, including `recurrence_details`.

#### Tests for Recurring Reminders ⚠️

-   [ ] T026 [P] Add test cases for `create_recurring_reminder` in `tests/unit/test_core.py`
-   [ ] T027 Implement test cases for "daily" recurrence in `tests/unit/test_core.py`
-   [ ] T028 Implement test cases for "weekly" recurrence in `tests/unit/test_core.py`
-   [ ] T029 Implement test cases for "monthly" recurrence in `tests/unit/test_core.py`
-   [ ] T030 Implement test cases for "yearly" recurrence in `tests/unit/test_core.py`
-   [ ] T031 Implement test cases for invalid `recurrence_type` or `recurrence_details` in `tests/unit/test_core.py`

#### Implementation for Recurring Reminders

-   [ ] T032 Implement `create_recurring_reminder` in `src/reminder_agent/core.py`

---

### Phase 7: Notification Callbacks and Utilities

**Goal**: Provide a mechanism for consuming applications to be notified when reminders are due.

**Independent Test**: Register a callback and verify it's triggered when a reminder's due time is reached (requires a mock time or scheduler).

#### Tests for Callbacks ⚠️

-   [ ] T033 [P] Create `tests/unit/test_callbacks.py` for notification callback mechanism
-   [ ] T034 Implement test case for `register_notification_callback` in `tests/unit/test_callbacks.py`
-   [ ] T035 Implement test case for `unregister_notification_callback` in `tests/unit/test_callbacks.py`
-   [ ] T036 Implement test case for triggering registered callbacks when a reminder is due in `tests/unit/test_callbacks.py`

#### Implementation for Callbacks

-   [ ] T037 [P] Create `src/reminder_agent/callbacks.py` for notification callback management
-   [ ] T038 Implement `register_notification_callback` in `src/reminder_agent/core.py` (delegating to `callbacks.py`)
-   [ ] T039 Implement `unregister_notification_callback` in `src/reminder_agent/core.py` (delegating to `callbacks.py`)
-   [ ] T040 Implement `get_reminder` in `src/reminder_agent/core.py`

---

### Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

-   [ ] T041 Code cleanup and refactoring across `src/reminder_agent/`
-   [ ] T042 Ensure all public API methods have docstrings and type hints
-   [ ] T043 Review and improve error handling (custom exceptions)
-   [ ] T044 Run `pytest --cov=reminder_agent` and aim for >80% code coverage (as per constitution)
-   [ ] T045 Create `tests/integration/test_integration.py` for end-to-end flows.
-   [ ] T046 Implement integration tests covering core user stories in `tests/integration/test_integration.py`
-   [ ] T047 Validate `quickstart.md` examples.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately.
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
-   **User Stories (Phase 3-7)**: All depend on Foundational phase completion.
    *   User Stories 1, 2, 3 can generally proceed in parallel after foundational, with some careful integration.
    *   Recurring reminders and callbacks build on the core features.
-   **Polish (Phase 8)**: Depends on all desired user stories being complete.

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2). No direct dependencies on other stories.
-   **User Story 2 (P1)**: Can start after Foundational (Phase 2). No direct dependencies on other stories, but will list reminders created by US1.
-   **User Story 3 (P2)**: Can start after Foundational (Phase 2). No direct dependencies on other stories, but will delete reminders created by US1.
-   **Recurring Reminders (Phase 6)**: Builds upon the basic `create_reminder` mechanism.
-   **Notification Callbacks (Phase 7)**: Builds upon the `ReminderManager` and due reminder detection.

### Within Each User Story

-   Tests MUST be written and FAIL before implementation.
-   Models before services.
-   Services before core logic.
-   Core implementation before integration.
-   Story complete before moving to next priority.

### Parallel Opportunities

-   All Setup tasks (T001-T004) can run in parallel.
-   Tasks T005, T006, T008, T009 in Foundational Phase can run in parallel.
-   Once Foundational phase completes, User Stories 1, 2, and 3 can be worked on in parallel by different team members.
-   Within each user story, test tasks (marked [P]) can run in parallel.
-   Within each user story, model creation (if any) can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
- [ ] T011 [P] [US1] Create `tests/unit/test_core.py` for `create_one_time_reminder`
- [ ] T012 [US1] Implement test case for valid one-time reminder creation in `tests/unit/test_core.py`
- [ ] T013 [US1] Implement test case for `ValueError` when `due_at` is in the past in `tests/unit/test_core.py`

# Launch core implementation:
- [ ] T014 [P] [US1] Create `src/reminder_agent/core.py` for `ReminderManager` class
- [ ] T015 [US1] Implement `ReminderManager.__init__` to accept `PersistenceAdapter` in `src/reminder_agent/core.py`
- [ ] T016 [US1] Implement `create_one_time_reminder` in `src/reminder_agent/core.py`
- [ ] T017 [US1] Ensure `create_one_time_reminder` validates `due_at` is in the future.
```

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (Set a One-Time Reminder)
4.  Complete Phase 4: User Story 2 (List All Pending Reminders)
5.  **STOP and VALIDATE**: Test User Stories 1 & 2 independently.
6.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Continue with Recurring Reminders and Callbacks.
6.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    *   Developer A: User Story 1 (Set One-Time Reminder)
    *   Developer B: User Story 2 (List Reminders)
    *   Developer C: User Story 3 (Delete Reminder)
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies.
-   [Story] label maps task to specific user story for traceability.
-   Each user story should be independently completable and testable.
-   Verify tests fail before implementing.
-   Commit after each task or logical group.
-   Stop at any checkpoint to validate story independently.
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.