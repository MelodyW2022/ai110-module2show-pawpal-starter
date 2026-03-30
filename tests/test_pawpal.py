import pytest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


@pytest.fixture
def owner():
    """Create a basic Owner."""
    return Owner("Alice")


@pytest.fixture
def pet(owner):
    """Create a basic Pet with an Owner."""
    p = Pet("Buddy", "Dog", 3, "No notes", owner)
    owner.add_pet(p)
    return p


@pytest.fixture
def task(pet):
    """Create a Task assigned to the pet fixture."""
    scheduled = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    return Task("Feed", "high", 10, pet, scheduled)


@pytest.fixture
def scheduler(owner):
    """Create a Scheduler for the owner fixture."""
    return Scheduler(owner)


# --- Test 1: Task Completion ---
def test_task_completion_changes_status(task):
    """Calling complete() should change status from 'pending' to 'completed'."""
    assert task.get_status() == "pending"
    assert task.is_completed() is False

    task.complete()

    assert task.get_status() == "completed"
    assert task.is_completed() is True


# --- Test 2: Task Addition ---
def test_add_task_increases_pet_task_count(pet, task):
    """Adding a task to a pet should increase its task count by one."""
    assert len(pet.get_care_tasks()) == 0

    pet.add_task(task)

    assert len(pet.get_care_tasks()) == 1


# --- Test 3: Sorting Correctness ---
def test_sort_by_time_returns_chronological_order(pet, scheduler):
    """Tasks added out of order should come back sorted earliest-first."""
    base = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    t_late  = Task("Walk",  "medium", 20, pet, base + timedelta(hours=2))
    t_early = Task("Feed",  "high",   10, pet, base)
    t_mid   = Task("Brush", "low",    15, pet, base + timedelta(hours=1))

    scheduler.add_task(t_late)
    scheduler.add_task(t_early)
    scheduler.add_task(t_mid)

    sorted_tasks = scheduler.sort_by_time(pet.get_care_tasks())

    assert sorted_tasks[0].get_title() == "Feed"
    assert sorted_tasks[1].get_title() == "Brush"
    assert sorted_tasks[2].get_title() == "Walk"


# --- Test 4a: Priority-based sorting ---
def test_generate_daily_schedule_sorts_by_priority_then_time(pet, scheduler):
    """High priority tasks should appear before lower priority tasks, with time as tiebreaker."""
    base = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    t_low    = Task("Grooming", "low",    15, pet, base)                         # low,    08:00
    t_high   = Task("Feed",     "high",   10, pet, base + timedelta(hours=1))    # high,   09:00
    t_medium = Task("Walk",     "medium", 20, pet, base + timedelta(minutes=30)) # medium, 08:30

    scheduler.add_task(t_low)
    scheduler.add_task(t_high)
    scheduler.add_task(t_medium)

    schedule = scheduler.generate_daily_schedule(base)

    assert schedule[0].get_title() == "Feed"      # high
    assert schedule[1].get_title() == "Walk"      # medium
    assert schedule[2].get_title() == "Grooming"  # low


# --- Test 4b: Time sorting when priorities are equal ---
def test_generate_daily_schedule_sorts_by_time_when_priority_equal(pet, scheduler):
    """When tasks share the same priority, they should be sorted by scheduled time."""
    base = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)

    t1 = Task("Dinner",    "high", 10, pet, base + timedelta(hours=5))
    t2 = Task("Breakfast", "high", 10, pet, base)

    scheduler.add_task(t1)
    scheduler.add_task(t2)

    schedule = scheduler.generate_daily_schedule(base)

    assert schedule[0].get_title() == "Breakfast"
    assert schedule[1].get_title() == "Dinner"


# --- Test 5: Daily recurrence ---
def test_daily_task_schedules_next_day(pet, scheduler):
    """Completing a daily task should auto-create a task for the next day."""
    base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    task = Task("Feed", "high", 10, pet, base, _frequency="daily")
    scheduler.add_task(task)

    next_task = scheduler.mark_task_complete(task)

    assert next_task is not None
    assert next_task.get_scheduled_time() == base + timedelta(days=1)
    assert next_task.get_title() == "Feed"
    assert next_task.get_frequency() == "daily"


# --- Test 6: Weekly recurrence ---
def test_weekly_task_schedules_next_week(pet, scheduler):
    """Completing a weekly task should auto-create a task seven days later."""
    base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    task = Task("Grooming", "medium", 30, pet, base, _frequency="weekly")
    scheduler.add_task(task)

    next_task = scheduler.mark_task_complete(task)

    assert next_task is not None
    assert next_task.get_scheduled_time() == base + timedelta(weeks=1)
    assert next_task.get_title() == "Grooming"
    assert next_task.get_frequency() == "weekly"


# --- Test 7: Non-recurring task returns None ---
def test_non_recurring_task_returns_none(pet, scheduler):
    """Completing a task with frequency 'none' should not create a follow-up task."""
    base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    task = Task("Vet visit", "high", 60, pet, base, _frequency="none")
    scheduler.add_task(task)

    result = scheduler.mark_task_complete(task)

    assert result is None
    assert task.is_completed() is True


# --- Test 8: Conflict detection — overlap ---
def test_add_task_detects_overlap(pet, scheduler):
    """Two tasks whose time windows overlap should trigger a conflict warning."""
    base = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)

    t1 = Task("Feed", "high", 30, pet, base)                                  # 10:00 – 10:30
    t2 = Task("Walk", "high", 20, pet, base + timedelta(minutes=15))          # 10:15 – 10:35

    scheduler.add_task(t1)
    result = scheduler.add_task(t2)

    assert "CONFLICT" in result
    assert len(pet.get_care_tasks()) == 1


# --- Test 9: No conflict when tasks are sequential ---
def test_add_task_no_conflict_when_sequential(pet, scheduler):
    """Tasks that don't overlap should both be added successfully."""
    base = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)

    t1 = Task("Feed", "high", 30, pet, base)                                  # 10:00 – 10:30
    t2 = Task("Walk", "high", 20, pet, base + timedelta(minutes=30))          # 10:30 – 10:50

    result1 = scheduler.add_task(t1)
    result2 = scheduler.add_task(t2)

    assert result1 == "ok"
    assert result2 == "ok"
    assert len(pet.get_care_tasks()) == 2


# --- Test 10: Edge case — pet with no tasks ---
def test_scheduler_handles_pet_with_no_tasks(owner, scheduler):
    """A pet with no tasks should not crash generate_daily_schedule."""
    empty_pet = Pet("Shadow", "Cat", 2, "Indoor only", owner)
    owner.add_pet(empty_pet)

    schedule = scheduler.generate_daily_schedule(datetime.now())

    assert isinstance(schedule, list)
    assert len(schedule) == 0
