from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta


class Owner:
    def __init__(self, name: str):
        self.__name: str = name
        self.__preferences: dict = {}
        self.__pets: list[Pet] = []

    def get_name(self) -> str:
        """Return the owner's name."""
        return self.__name

    def set_name(self, name: str) -> None:
        """Update the owner's name."""
        self.__name = name

    def get_preference(self, key: str):
        """Return the preference value for the given key, or None if not set."""
        return self.__preferences.get(key)

    def set_preference(self, key: str, value) -> None:
        """Set or update a preference key-value pair."""
        self.__preferences[key] = value

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.__pets

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.__pets.append(pet)


@dataclass
class Pet:
    _name: str
    _species: str
    _age: int
    _care_notes: str
    _owner: Owner
    _tasks: list[Task] = field(default_factory=list)

    def get_name(self) -> str:
        """Return the pet's name."""
        return self._name

    def set_name(self, name: str) -> None:
        """Update the pet's name."""
        self._name = name

    def get_species(self) -> str:
        """Return the pet's species."""
        return self._species

    def get_age(self) -> int:
        """Return the pet's age."""
        return self._age

    def set_age(self, age: int) -> None:
        """Update the pet's age."""
        self._age = age

    def get_care_notes(self) -> str:
        """Return the pet's care notes."""
        return self._care_notes

    def update_care_notes(self, notes: str) -> None:
        """Replace the pet's care notes with new text."""
        self._care_notes = notes

    def get_owner(self) -> Owner:
        """Return the owner responsible for this pet."""
        return self._owner

    def set_owner(self, owner: Owner) -> None:
        """Reassign this pet to a different owner."""
        self._owner = owner

    def get_care_tasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return self._tasks

    def add_task(self, task: Task) -> None:
        # Single storage point for tasks — only called by Scheduler.add_task() after conflict checking
        """Append a task to this pet's task list."""
        self._tasks.append(task)


@dataclass
class Task:
    _title: str
    _priority: str
    _duration_minutes: int
    _assigned_pet: Pet
    _scheduled_time: datetime
    _status: str = "pending"
    _frequency: str = "none"

    def get_title(self) -> str:
        """Return the task title."""
        return self._title

    def set_title(self, title: str) -> None:
        """Update the task title."""
        self._title = title

    def get_priority(self) -> str:
        """Return the task priority level."""
        return self._priority

    def set_priority(self, priority: str) -> None:
        """Update the task priority level."""
        self._priority = priority

    def get_duration(self) -> int:
        """Return the task duration in minutes."""
        return self._duration_minutes

    def set_duration(self, minutes: int) -> None:
        """Update the task duration in minutes."""
        self._duration_minutes = minutes

    def get_assigned_pet(self) -> Pet:
        """Return the pet this task is assigned to."""
        return self._assigned_pet

    def set_assigned_pet(self, pet: Pet) -> None:
        """Reassign this task to a different pet."""
        self._assigned_pet = pet

    def get_scheduled_time(self) -> datetime:
        """Return the datetime this task is scheduled for."""
        return self._scheduled_time

    def schedule(self, time: datetime) -> None:
        """Set or update the scheduled datetime for this task."""
        self._scheduled_time = time

    def get_status(self) -> str:
        """Return the current completion status of the task."""
        return self._status

    def complete(self) -> None:
        """Mark this task as completed."""
        self._status = "completed"

    def is_completed(self) -> bool:
        """Return True if the task has been completed."""
        return self._status == "completed"

    def get_frequency(self) -> str:
        """Return the recurrence frequency: 'none', 'daily', or 'weekly'."""
        return self._frequency

    def set_frequency(self, frequency: str) -> None:
        """Set the recurrence frequency: 'none', 'daily', or 'weekly'."""
        self._frequency = frequency


class Scheduler:
    def __init__(self, owner: Owner):
        self.__owner: Owner = owner

    def get_owner(self) -> Owner:
        pass

    def set_owner(self, owner: Owner) -> None:
        pass

    def get_tasks_for_day(self, date: datetime) -> list[Task]:
        """Return all tasks across all pets scheduled on the given date."""
        result = []
        for pet in self.__owner.get_pets():
            for task in pet.get_care_tasks():
                if task.get_scheduled_time().date() == date.date():
                    result.append(task)
        return result

    def add_task(self, task: Task) -> None:
        # Call __check_conflicts() first; if no conflict, delegate storage to task.get_assigned_pet().add_task(task)
        """Add a task to its assigned pet after checking for scheduling conflicts."""
        if not self.__check_conflicts(task, task.get_scheduled_time()):
            task.get_assigned_pet().add_task(task)

    def __check_conflicts(self, task: Task, time: datetime) -> bool:
        # Internal guard called by add_task() only — checks existing tasks across all pets for time conflicts
        """Return True if any existing task overlaps with the given task's time slot."""
        for pet in self.__owner.get_pets():
            for existing in pet.get_care_tasks():
                existing_start = existing.get_scheduled_time()
                existing_start_minutes = existing_start.timestamp() / 60
                existing_end_minutes = existing_start_minutes + existing.get_duration()
                new_start_minutes = time.timestamp() / 60
                new_end_minutes = new_start_minutes + task.get_duration()
                if not (new_end_minutes <= existing_start_minutes or
                        new_start_minutes >= existing_end_minutes):
                    return True
        return False

    def generate_daily_schedule(self, date: datetime) -> list[Task]:
        """Return tasks for the given date sorted by scheduled time."""
        return sorted(self.get_tasks_for_day(date), key=lambda t: t.get_scheduled_time())

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task complete and auto-schedule the next occurrence if recurring.

        Returns the newly created Task if one was created, otherwise None.
        """
        task.complete()
        if task.get_frequency() == "daily":
            delta = timedelta(days=1)
        elif task.get_frequency() == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None
        next_task = Task(
            _title=task.get_title(),
            _priority=task.get_priority(),
            _duration_minutes=task.get_duration(),
            _assigned_pet=task.get_assigned_pet(),
            _scheduled_time=task.get_scheduled_time() + delta,
            _frequency=task.get_frequency(),
        )
        self.add_task(next_task)
        return next_task

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return a new list of tasks sorted by scheduled time (earliest first)."""
        return sorted(tasks, key=lambda t: t.get_scheduled_time())

    def filter_by_pet(self, tasks: list[Task], pet_name: str) -> list[Task]:
        """Return only the tasks assigned to the pet with the given name."""
        return [t for t in tasks if t.get_assigned_pet().get_name() == pet_name]

    def filter_by_status(self, tasks: list[Task], status: str) -> list[Task]:
        """Return only the tasks matching the given status ('pending' or 'completed')."""
        return [t for t in tasks if t.get_status() == status]
