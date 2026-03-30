import pytest
from datetime import datetime
from pawpal_system import Owner, Pet, Task


@pytest.fixture
def pet():
    """Create a basic Pet with an Owner."""
    owner = Owner("Alice")
    return Pet("Buddy", "Dog", 3, "No notes", owner)


@pytest.fixture
def task(pet):
    """Create a Task assigned to the pet fixture."""
    scheduled = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    return Task("Feed", "high", 10, pet, scheduled)


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
