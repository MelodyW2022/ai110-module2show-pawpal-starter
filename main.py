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
    today.replace(hour=12, minute=0, second=0, microsecond=0),
)

feed_buddy = Task(
    "Feed Buddy",
    "high",
    10,
    buddy,
    today.replace(hour=8, minute=0, second=0, microsecond=0),
)

feed_whiskers = Task(
    "Feed Whiskers",
    "medium",
    10,
    whiskers,
    today.replace(hour=17, minute=00, second=0, microsecond=0),
)

groom = Task(
    "Groom Whiskers",
    "low",
    20,
    whiskers,
    today.replace(hour=12, minute=30, second=0, microsecond=0),
)

for task in [walk, feed_buddy, feed_whiskers, groom]:
    scheduler.add_task(task)

# --- Mark some tasks complete for demo purposes ---
walk.complete()
feed_buddy.complete()

# --- Conflict Detection Demo ---
conflicting_task = Task(
    "Vet Appointment",
    "high",
    20,
    buddy,
    today.replace(hour=8, minute=5, second=0, microsecond=0),
)
result = scheduler.add_task(conflicting_task)
print(f"\n--- Conflict Detection ---")
print(f"  {result}")

# --- Recurring Task Demo ---
evening_feed = Task(
    "Evening Feed",
    "high",
    10,
    buddy,
    today.replace(hour=18, minute=0, second=0, microsecond=0),
    _frequency="daily",
)
scheduler.add_task(evening_feed)

print("\n--- Recurring Task: mark complete and auto-schedule next ---")
next_task = scheduler.mark_task_complete(evening_feed)
if next_task:
    fmt = "%b %d, %Y %I:%M %p"
    print(f"  '{evening_feed.get_title()}' completed — {evening_feed.get_scheduled_time().strftime(fmt)}, {evening_feed.get_duration()} min")
    print(f"  Next occurrence auto-scheduled: {next_task.get_scheduled_time().strftime(fmt)}, {next_task.get_duration()} min")

# --- Sorting and Filtering Demo ---
all_tasks = []
for pet in owner.get_pets():
    all_tasks.extend(pet.get_care_tasks())

print("\n--- Filter: Buddy's tasks only ---")
buddy_tasks = scheduler.filter_by_pet(all_tasks, "Buddy")
for t in scheduler.sort_by_time(buddy_tasks):
    status = "[x]" if t.is_completed() else "[ ]"
    print(f"  {status} {t.get_scheduled_time().strftime('%b %d, %Y %I:%M %p')}  [{t.get_priority().upper()}]  {t.get_title()} ({t.get_assigned_pet().get_name()})  — {t.get_duration()} min")

print("\n--- Filter: completed tasks ---")
for t in scheduler.sort_by_time(scheduler.filter_by_status(all_tasks, "completed")):
    print(f"  [x] {t.get_scheduled_time().strftime('%b %d, %Y %I:%M %p')}  [{t.get_priority().upper()}]  {t.get_title()} ({t.get_assigned_pet().get_name()})  — {t.get_duration()} min")

print("\n--- Filter: pending tasks ---")
for t in scheduler.sort_by_time(scheduler.filter_by_status(all_tasks, "pending")):
    print(f"  [ ] {t.get_scheduled_time().strftime('%b %d, %Y %I:%M %p')}  [{t.get_priority().upper()}]  {t.get_title()} ({t.get_assigned_pet().get_name()})  — {t.get_duration()} min")

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
