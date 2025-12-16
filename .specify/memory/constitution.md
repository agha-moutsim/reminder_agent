<!--
Sync Impact Report:
Version change: Initial creation -> 1.0.0
List of modified principles:
  - TDD Approach
  - Pythonic Code & Type Safety
  - Architectural Decision Records (ADRs)
  - OOP Principles
  - Version Control
  - Quality Assurance
Added sections:
  - Technical Stack
  - Quality Requirements
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .gemini/commands/sp.adr.toml ⚠ pending
  - .gemini/commands/sp.analyze.toml ⚠ pending
  - .gemini/commands/sp.checklist.toml ⚠ pending
  - .gemini/commands/sp.clarify.toml ⚠ pending
  - .gemini/commands/sp.constitution.toml ✅ updated
  - .gemini/commands/sp.git.commit_pr.toml ⚠ pending
  - .gemini/commands/sp.implement.toml ⚠ pending
  - .gemini/commands/sp.phr.toml ⚠ pending
  - .gemini/commands/sp.plan.toml ⚠ pending
  - .gemini/commands/sp.specify.toml ⚠ pending
  - .gemini/commands/sp.tasks.toml ⚠ pending
Follow-up TODOs: None
-->
# Reminder Agent Project Constitution

## Core Principles

### I. TDD Approach
All development must follow a Test-Driven Development (TDD) approach. Tests must be written and approved before implementation, strictly adhering to the Red-Green-Refactor cycle.

### II. Pythonic Code & Type Safety
All Python code must be written using Python 3.12+ and include comprehensive type hints. Code should be clean, readable, and adhere to established Python best practices.

### III. Architectural Decision Records (ADRs)
All significant architectural decisions must be documented using Architectural Decision Records (ADRs) to capture context, rationale, and consequences.

### IV. OOP Principles
Adhere to essential Object-Oriented Programming (OOP) principles: SOLID, DRY (Don't Repeat Yourself), and KISS (Keep It Simple, Stupid).

### V. Version Control
All project files, including code, documentation, and configuration, must be managed under Git version control.

### VI. Quality Assurance
All tests must pass with at least 80% code coverage. Dataclasses should be used for data structures to ensure clarity and type safety.

## Technical Stack

- Python 3.12+
- UV package manager
- pytest for testing

## Quality Requirements

- All tests must pass.
- At least 80% code coverage.
- Use dataclasses for data structures.

## Governance

- The constitution supersedes all other project practices.
- Amendments require documentation, approval, and a migration plan.
- All Pull Requests (PRs) and reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
