# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The three core actions a user should be able to perform in PawPal+ are:

1. **Add a pet** — A user can register a pet by providing details such as the pet's name, species, age, and any special care notes. This action creates a Pet record in the system that all other features (scheduling, tasks) are built around.

2. **Schedule a walk** — A user can create a walk event for a specific pet by choosing a date, time, and duration. The scheduler checks for conflicts and assigns the walk to an available time slot, ensuring the pet's exercise needs are met consistently.

3. **See today's tasks** — A user can view a consolidated list of all care tasks due today across all their pets (walks, feedings, vet appointments, etc.). This gives the owner a clear daily overview so nothing is missed.

**Initial UML design:**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The initial design included four main classes:

- **`Owner`** — represents the pet owner and manages their collection of pets.
  - **Attributes**: name (str), preferences (dict), pets (list of Pet)
  - **Methods**: add_pet(pet), get_pets(), set_preference(key, value), get_preference(key)

- **`Pet`** — stores pet information and belongs to an owner.
  - **Attributes**: name (str), species (str), age (int), care_notes (str), owner (Owner)
  - **Methods**: get_care_tasks(), update_care_notes(notes), get_owner()

- **`Task`** — represents a scheduled care activity for a pet.
  - **Attributes**: title (str), duration_minutes (int), priority (str: "low"/"medium"/"high"), assigned_pet (Pet), scheduled_time (datetime), status (str: "pending"/"completed")
  - **Methods**: schedule(time), complete(), get_duration(), is_completed()

- **`Scheduler`** — manages task scheduling and conflict resolution.
  - **Attributes**: owner (Owner), tasks (list of Task)
  - **Methods**: generate_daily_schedule(), check_conflicts(task, time), add_task(task), get_tasks_for_day(date)

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, several changes were made during the design review — some suggested by AI, others identified by me.

**Changes suggested by AI:**

1. **`check_conflicts` made private** — AI suggested making it private since it is an internal guard called only inside `add_task()`. This prevents callers from bypassing the conflict check by calling `add_task()` without it. I questioned this and AI explained the reasoning, which I accepted.

2. **`@dataclass` incompatible with double-underscore attributes** — AI identified that Python's name mangling turns `__name` into `_Pet__name` internally, which breaks the auto-generated `__init__` in dataclasses. Changed `Pet` and `Task` attributes to single underscore `_` (convention-based private) to fix the incompatibility.

3. **Removed `tasks` attribute from `Scheduler`** — AI identified that `Scheduler` maintaining its own flat list of tasks alongside `Pet` also storing tasks was a data sync risk. Since `Pet` owns tasks (composition), `Scheduler` now derives all tasks by navigating `owner → pets → tasks` rather than holding a duplicate list.

4. **Added `date` parameter to `generate_daily_schedule()`** — AI identified that without a `date` parameter, it was unclear which day the method generates a schedule for. Added `date: datetime` to make it consistent with `get_tasks_for_day(date)`.

5. **Clarified `add_task()` responsibility between `Scheduler` and `Pet`** — AI identified that both `Scheduler.add_task()` and `Pet.add_task()` being stubs created an ambiguity — if tasks could be added via `Pet` directly, conflict checking in `Scheduler` would be bypassed. Established that `Scheduler.add_task()` is the entry point (runs `__check_conflicts()` first, then delegates to `pet.add_task()`), while `Pet.add_task()` is the single storage point only called by `Scheduler`.

**Changes I identified:**

1. **All attributes made private** — I decided that all attributes should be private to properly enforce encapsulation, not just the ones AI initially flagged.

2. **Added getters and setters** — Since all attributes are private, other classes need public methods to access them. Getters were added for all attributes. Setters were added only where external modification is valid — attributes already controlled by dedicated methods (e.g., `status` via `complete()`, `care_notes` via `update_care_notes()`) did not get raw setters to avoid bypassing business logic.

3. **Relationship types refined to composition** — I identified that `Owner → Pet` and `Pet → Task` are composition relationships (the child cannot exist without the parent), represented as `*--` in Mermaid, while `Scheduler → Owner` remains an association (`-->`) since Scheduler references but does not own the Owner.

4. **Added `tasks` attribute and `add_task()` to `Pet`** — I noticed that `Owner` holds a list of `Pet` objects, but `Pet` had no corresponding `tasks` list despite owning Tasks in a composition relationship. Added `-tasks: list[Task]` and `+add_task(task)` to `Pet` to mirror the Owner→Pet pattern consistently.

5. **Added setters for `Task.assigned_pet` and `Scheduler.owner`** — AI initially omitted setters for these, but I challenged this. A task could be reassigned to a different pet, and a scheduler may need to switch owners for flexibility. After discussion, setters were added for both.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
