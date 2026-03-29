from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner("Alice")

buddy = Pet("Buddy", "Dog", 3, "Allergic to chicken", owner)
whiskers = Pet("Whiskers", "Cat", 5, "Indoor only", owner)

owner.add_pet(buddy)
owner.add_pet(whiskers)

scheduler = Scheduler(owner)

# --- Tasks (all scheduled for today) ---
today = datetime.now()

walk = Task(
    "Morning Walk",
    "high",
    30,
    buddy,
    today.replace(hour=8, minute=0, second=0, microsecond=0),
)

feed_buddy = Task(
    "Feed Buddy",
    "high",
    10,
    buddy,
    today.replace(hour=12, minute=0, second=0, microsecond=0),
)

feed_whiskers = Task(
    "Feed Whiskers",
    "medium",
    10,
    whiskers,
    today.replace(hour=12, minute=30, second=0, microsecond=0),
)

groom = Task(
    "Groom Whiskers",
    "low",
    20,
    whiskers,
    today.replace(hour=17, minute=0, second=0, microsecond=0),
)

for task in [walk, feed_buddy, feed_whiskers, groom]:
    scheduler.add_task(task)

# --- Print Today's Schedule ---
schedule = scheduler.generate_daily_schedule(today)

print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)
for task in schedule:
    time_str = task.get_scheduled_time().strftime("%I:%M %p")
    status = "[x]" if task.is_completed() else "[ ]"
    print(
        f"{status} {time_str}  [{task.get_priority().upper()}]"
        f"  {task.get_title()} ({task.get_assigned_pet().get_name()})"
        f"  — {task.get_duration()} min"
    )
print("=" * 40)
