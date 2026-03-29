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

The initial design included four main classes. All attributes are private (encapsulated) and accessed through public getters and setters. Setters are only added where external modification makes sense; attributes controlled by dedicated methods do not have raw setters.

- **`Owner`** — represents the pet owner and manages their collection of pets.
  - **Attributes** (all private): `name` (str), `preferences` (dict), `pets` (list of Pet)
  - **Methods**:
    - `get_name()`, `set_name(name)`
    - `get_preference(key)`, `set_preference(key, value)`
    - `get_pets()`, `add_pet(pet)` — `pets` has no raw setter; `add_pet()` controls all additions

- **`Pet`** — stores pet information, belongs to an owner, and owns a collection of tasks.
  - **Attributes** (all private): `name` (str), `species` (str), `age` (int), `care_notes` (str), `owner` (Owner), `tasks` (list of Task)
  - **Methods**:
    - `get_name()`, `set_name(name)`
    - `get_species()` — species never changes, no setter
    - `get_age()`, `set_age(age)`
    - `get_care_notes()`, `update_care_notes(notes)` — dedicated method acts as setter
    - `get_owner()`, `set_owner(owner)`
    - `get_care_tasks()`, `add_task(task)` — `tasks` has no raw setter

- **`Task`** — represents a scheduled care activity for a pet.
  - **Attributes** (all private): `title` (str), `priority` (str: "low"/"medium"/"high"), `duration_minutes` (int), `assigned_pet` (Pet), `scheduled_time` (datetime), `status` (str: "pending"/"completed")
  - **Methods**:
    - `get_title()`, `set_title(title)`
    - `get_priority()`, `set_priority(priority)`
    - `get_duration()`, `set_duration(minutes)`
    - `get_assigned_pet()`, `set_assigned_pet(pet)`
    - `get_scheduled_time()`, `schedule(time)` — dedicated method acts as setter
    - `get_status()`, `complete()` — status controlled via `complete()` to enforce valid transitions; `is_completed()` for boolean check

- **`Scheduler`** — manages task scheduling and conflict resolution for an owner.
  - **Attributes** (all private): `owner` (Owner), `tasks` (list of Task)
  - **Methods**:
    - `get_owner()`, `set_owner(owner)`
    - `get_tasks_for_day(date)`, `add_task(task)`, `__check_conflicts(task, time)` (private — internal guard called inside `add_task()`)
    - `generate_daily_schedule()` — higher-level operation that produces the full day's schedule

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, several changes were made during the design review — some suggested by AI, others identified by me.

**Changes suggested by AI:**

1. **Added getters and setters** — Once attributes were made private, AI raised that other classes would have no way to access them without public methods. Getters were added for all attributes. Setters were added only where external modification is valid — attributes already controlled by dedicated methods (e.g., `status` via `complete()`, `care_notes` via `update_care_notes()`) did not get raw setters to avoid bypassing business logic.

2. **`check_conflicts` made private** — AI suggested making it private since it is an internal guard called only inside `add_task()`. This prevents callers from bypassing the conflict check by calling `add_task()` without it. I questioned this and AI explained the reasoning, which I accepted.

3. **Relationship types refined to composition** — AI identified that `Owner → Pet` and `Pet → Task` are composition relationships (the child cannot exist without the parent), represented as `*--` in Mermaid, while `Scheduler → Owner` and `Scheduler → Task` remain associations (`-->`) since Scheduler references but does not own them.

**Changes I identified:**

1. **All attributes made private** — I decided that all attributes should be private to properly enforce encapsulation, not just the ones AI initially flagged.

2. **Added `tasks` attribute and `add_task()` to `Pet`** — I noticed that `Owner` holds a list of `Pet` objects, but `Pet` had no corresponding `tasks` list despite owning Tasks in a composition relationship. I added `-tasks: list[Task]` and `+add_task(task)` to `Pet` to mirror the Owner→Pet pattern consistently.

3. **Added setters for `Task.assigned_pet` and `Scheduler.owner`** — AI initially omitted setters for these, but I challenged this. A task could be reassigned to a different pet, and a scheduler may need to switch owners for flexibility. After discussion, setters were added for both.

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
