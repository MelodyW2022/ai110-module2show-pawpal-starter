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

  The scheduler considers two constraints: **time** (no two tasks can overlap in the same time window) and **recurrence** (daily/weekly frequency determines when the next occurrence is scheduled). Priority is stored on each task and used for display and filtering but is not used to auto-resolve conflicts or reorder tasks — that was a deliberate scope decision.

- How did you decide which constraints mattered most?

  Time was chosen as the most important constraint because it is the hard requirement: two care activities physically cannot happen simultaneously. Priority is softer — a high-priority task being scheduled late is still valid, whereas two tasks at the same time is always invalid.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

  The scheduler checks for time overlaps across **all pets**, not just the pet being assigned the task. This means if Buddy has a task at 8:00 AM, you cannot schedule Whiskers at 8:05 AM either — even though a real owner could theoretically handle two short tasks close together or delegate one.

- Why is that tradeoff reasonable for this scenario?

  This is reasonable for a single-owner app because the owner is the only caregiver. It is simpler and safer to over-block than to allow overlaps that could cause the owner to miss a task. If multi-caregiver support were added later, the conflict scope could be narrowed to per-pet.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

  AI tools (Claude Code) were used across several roles: **design brainstorming** (reviewing the initial UML and identifying gaps like the missing `tasks` attribute on `Pet`), **code generation** (drafting initial test stubs), and **refactoring** (asking whether `get_conflicting_task` should be public or private and why).

- What kinds of prompts or questions were most helpful?
  The most helpful prompt pattern was asking **"why"** questions rather than just "fix this" — for example: _"Why would removing the duplicate task list from Scheduler improve the design?"_ This forced a reasoned explanation I could evaluate rather than blindly accepting a code change.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

  Copilot initially omitted setters for `Task.assigned_pet` and `Scheduler.owner`, reasoning that these associations rarely change after creation. I challenged this because a task could be reassigned to a different pet, and a scheduler might need to switch owners. I verified by tracing how the object graph would need to mutate across real use cases, then overrode the suggestion and added both setters.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

  The suite covers five categories: task lifecycle (`complete()` flips status from `pending` to `completed`), sorting correctness (`sort_by_time` and `generate_daily_schedule` return tasks in chronological order regardless of insertion order), recurrence logic (daily → +1 day, weekly → +7 days, none → `None` with no follow-up), conflict detection (overlapping tasks are blocked and not added, sequential tasks both pass), and an edge case (a pet with zero tasks does not crash `generate_daily_schedule`).

  These were important because they target the three features that required the most algorithmic logic — sorting, recurrence, and conflict detection — and confirm the system fails gracefully on empty input rather than raising unexpected exceptions.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

  ★★★★★ — Confidence is high for the behaviors covered. All 10 tests pass.

  Next edge cases to test would be: a task whose duration spans midnight (edge of `timedelta` arithmetic), two pets with tasks at the exact same time (confirming cross-pet conflict detection works correctly), and completing a recurring task that itself conflicts with an already-scheduled task on the next day.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

  The encapsulation design worked well throughout the project. Making all attributes private and routing all mutations through dedicated methods (e.g., `complete()` instead of a raw status setter) meant that each method's behavior was easy to reason about in isolation and test independently. The decision to make `Scheduler` the single entry point for adding tasks — delegating storage to `Pet.add_task()` only after conflict checking — prevented the kind of data integrity bugs that would have been hard to trace later.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

  I would add priority-based conflict resolution: instead of simply blocking a conflicting task, the scheduler could compare priorities and either suggest a nearby open time slot or ask the owner whether to bump the lower-priority task. This would make the scheduler feel more like an intelligent assistant rather than a hard gate.

  I would also add a "Mark Complete" button in the UI so the recurrence feature is fully visible to the user — right now frequency can be set but the auto-scheduling of the next occurrence is only verifiable through the test suite, not the app itself.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

  The most important thing I learned is that **AI is a fast executor but a poor architect without direction**. Left unconstrained, AI generated reasonable-looking code that had subtle design problems — duplicate state, missing encapsulation, ambiguous responsibilities. The value I added as the lead architect was not writing more code, but asking the right questions: *Who owns this data? What happens if this method is called out of order? What breaks if I skip this step?* AI accelerated the build, but the design decisions that made the system correct and maintainable came from deliberate human judgment at each step.
