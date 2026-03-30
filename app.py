import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)
care_notes = st.text_input("Care notes", value="Loves morning walks")

if st.button("Add pet"):
    new_pet = Pet(
        _name=pet_name,
        _species=species,
        _age=age,
        _care_notes=care_notes,
        _owner=st.session_state.owner,
    )
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added {pet_name} the {species}!")

pets = st.session_state.owner.get_pets()
if pets:
    st.write("**Current pets:**", [p.get_name() for p in pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Schedule a Task ---
st.subheader("Schedule a Task")

if not pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    pet_names = [p.get_name() for p in pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)
    selected_pet = next(p for p in pets if p.get_name() == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        task_time = st.time_input("Scheduled time", value=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0).time())
    with col5:
        frequency = st.selectbox("Recurrence", ["none", "daily", "weekly"])

    task_datetime = datetime.combine(datetime.today(), task_time)

    if st.button("Add task"):
        new_task = Task(
            _title=task_title,
            _priority=priority,
            _duration_minutes=int(duration),
            _assigned_pet=selected_pet,
            _scheduled_time=task_datetime,
            _frequency=frequency,
        )
        result = st.session_state.scheduler.add_task(new_task)
        if result == "ok":
            st.success(f"Task '{task_title}' added for {selected_pet_name} at {task_time}.")
        else:
            st.warning(result)

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    schedule = st.session_state.scheduler.generate_daily_schedule(datetime.today())
    if schedule:
        st.success(f"Schedule for today ({datetime.today().strftime('%A, %B %d')}) — {len(schedule)} task(s), sorted by time:")
        rows = []
        for task in schedule:
            rows.append({
                "Time": task.get_scheduled_time().strftime("%I:%M %p"),
                "Task": task.get_title(),
                "Pet": task.get_assigned_pet().get_name(),
                "Duration (min)": task.get_duration(),
                "Priority": task.get_priority(),
                "Recurrence": task.get_frequency(),
                "Status": task.get_status(),
            })
        st.table(rows)
    else:
        st.info("No tasks scheduled for today. Add some tasks above.")
