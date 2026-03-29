# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The three core actions a user should be able to perform in PawPal+ are:

1. **Add a pet** — A user can register a pet by providing details such as the pet's name, species, age, and any special care notes. This action creates a Pet record in the system that all other features (scheduling, tasks) are built around.

2. **Schedule a walk** — A user can create a walk event for a specific pet by choosing a date, time, and duration. The scheduler checks for conflicts and assigns the walk to an available time slot, ensuring the pet's exercise needs are met consistently.

3. **See today's tasks** — A user can view a consolidated list of all care tasks due today across all their pets (walks, feedings, vet appointments, etc.). This gives the owner a clear daily overview so nothing is missed.

**Initial UML design:**

The initial design included three main classes:
- `Pet` — stores pet attributes (name, species, age, care notes) and serves as the central entity other classes reference.
- `Task` — represents a scheduled care activity (type, assigned pet, date/time, duration, status), responsible for tracking what needs to be done and when.
- `Scheduler` — manages the collection of tasks, handles conflict detection, and generates the daily task view for the user.

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
