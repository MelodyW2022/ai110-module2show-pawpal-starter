# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ includes algorithmic features that make scheduling more intelligent:

- **Sorting** — Tasks are sorted by scheduled time (earliest first) using `Scheduler.sort_by_time()`.
- **Filtering** — Tasks can be filtered by pet name (`filter_by_pet()`) or completion status (`filter_by_status()`), making it easy to view only what's relevant.
- **Recurring tasks** — Tasks can be marked as `"daily"` or `"weekly"`. When completed via `Scheduler.mark_task_complete()`, the next occurrence is automatically scheduled using Python's `timedelta`.
- **Conflict detection** — `Scheduler.add_task()` checks all existing tasks across all pets for time overlaps before adding a new task. If a conflict is found, a descriptive warning message is returned instead of silently skipping or crashing.

## Testing PawPal+

### How to run tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | What it verifies |
|------|-----------------|
| `test_task_completion_changes_status` | `complete()` flips status from `pending` to `completed` |
| `test_add_task_increases_pet_task_count` | Adding a task to a pet increments its task list |
| `test_sort_by_time_returns_chronological_order` | `sort_by_time()` returns tasks earliest-first regardless of insertion order |
| `test_generate_daily_schedule_is_sorted` | `generate_daily_schedule()` returns today's tasks in time order |
| `test_daily_task_schedules_next_day` | Completing a daily task auto-creates the next occurrence 1 day later |
| `test_weekly_task_schedules_next_week` | Completing a weekly task auto-creates the next occurrence 7 days later |
| `test_non_recurring_task_returns_none` | Completing a one-time task returns `None` (no follow-up created) |
| `test_add_task_detects_overlap` | Overlapping tasks trigger a `CONFLICT` warning and are not added |
| `test_add_task_no_conflict_when_sequential` | Back-to-back tasks with no overlap are both added successfully |
| `test_scheduler_handles_pet_with_no_tasks` | A pet with zero tasks does not crash `generate_daily_schedule` |

### Confidence level

★★★★★ — All 10 tests pass. Core behaviors (sorting, recurrence, conflict detection) and edge cases (empty task list, non-recurring tasks) are verified.
