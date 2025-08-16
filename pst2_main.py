# pst2_main.py - The Persistent Application (Fragments 2.1 ~ 2.3)
import json
import datetime  # used for attendance timestamps

DATA_FILE = "msms.json"
app_data = {}  # global dictionary holding all application data

# --- Core Persistence Engine (Fragment 2.1) ---
def load_data(path=DATA_FILE):
    """Load all application data from a JSON file.
    If the file does not exist, initialize with default structure.
    Mutates the existing 'app_data' dict in place to keep external references valid.
    """
    global app_data
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

    # mutate in place
    app_data.clear()
    app_data.update(data)


def save_data(path=DATA_FILE):
    """Save all application data to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(app_data, f, indent=4, ensure_ascii=False)
    print("Data saved successfully.")


# --- CRUD: Teachers & Students (Fragment 2.2) ---

def add_teacher(name: str, speciality: str) -> dict:
    """Create a new teacher and append to app_data['teachers'].""" 
    teacher = {
        "id": app_data["next_teacher_id"],
        "name": name,
        "speciality": speciality
    }
    app_data["teachers"].append(teacher)
    app_data["next_teacher_id"] += 1
    print(f"Core: Teacher '{name}' added (id={teacher['id']}).")
    return teacher


def update_teacher(teacher_id: int, **fields) -> bool:
    """Update teacher fields by id. Returns True if updated, else False."""
    for t in app_data["teachers"]:
        if t["id"] == teacher_id:
            t.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return True
    print(f"Error: Teacher with ID {teacher_id} not found.")
    return False


def remove_teacher(teacher_id: int) -> bool:
    """Remove a teacher by id. Returns True if removed, else False."""
    before = len(app_data["teachers"])
    app_data["teachers"] = [t for t in app_data["teachers"] if t["id"] != teacher_id]
    removed = len(app_data["teachers"]) < before
    if removed:
        print(f"Teacher {teacher_id} removed.")
    else:
        print(f"Error: Teacher with ID {teacher_id} not found.")
    return removed


def add_student(name: str, enrolled_in=None) -> dict:
    """Create a new student and append to app_data['students'].""" 
    if enrolled_in is None:
        enrolled_in = []
    student = {
        "id": app_data["next_student_id"],
        "name": name,
        "enrolled_in": list(enrolled_in),
    }
    app_data["students"].append(student)
    app_data["next_student_id"] += 1
    print(f"Core: Student '{name}' added (id={student['id']}).")
    return student


def update_student(student_id: int, **fields) -> bool:
    """Update student fields by id. Returns True if updated, else False."""
    for s in app_data["students"]:
        if s["id"] == student_id:
            s.update(fields)
            print(f"Student {student_id} updated.")
            return True
    print(f"Error: Student with ID {student_id} not found.")
    return False


def remove_student(student_id: int) -> bool:
    """Remove a student by id. Returns True if removed, else False."""
    before = len(app_data["students"])
    app_data["students"] = [s for s in app_data["students"] if s["id"] != student_id]
    removed = len(app_data["students"]) < before
    if removed:
        print(f"Student {student_id} removed.")
    else:
        print(f"Error: Student with ID {student_id} not found.")
    return removed


# --- Receptionist Features (Fragment 2.3) ---

def check_in(student_id: int, course_id: str, timestamp: str | None = None) -> dict:
    """Record a student's attendance in app_data['attendance'].""" 
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()

    record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp,
    }
    app_data["attendance"].append(record)
    print(f"Reception: Student {student_id} checked in to '{course_id}' at {timestamp}.")
    return record


def print_student_card(student_id: int) -> str:
    """Create a text badge for a student at '<student_id>_card.txt'.
    Returns the file path; raises ValueError if student not found.
    """
    student = next((s for s in app_data["students"] if s["id"] == student_id), None)
    if not student:
        msg = f"Student with ID {student_id} not found."
        print(f"Error: {msg}")
        raise ValueError(msg)

    filename = f"{student_id}_card.txt"
    lines = [
        "========================\n",
        "  MUSIC SCHOOL ID BADGE\n",
        "========================\n",
        f"ID: {student['id']}\n",
        f"Name: {student['name']}\n",
        f"Enrolled In: {', '.join(student.get('enrolled_in', []))}\n",
    ]
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Printed student card to {filename}.")
    return filename
# --- CLI Main Loop (Fragment 2.4) ---
def _input_int(prompt: str) -> int:
    """Read an integer from stdin; reprompt until valid."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.")

def _list_students():
    if not app_data.get("students"):
        print("(no students)")
        return
    print("Students:")
    for s in app_data["students"]:
        courses = ", ".join(s.get("enrolled_in", []))
        print(f"  ID={s['id']}, Name={s['name']}, Enrolled In=[{courses}]")

def _list_teachers():
    if not app_data.get("teachers"):
        print("(no teachers)")
        return
    print("Teachers:")
    for t in app_data["teachers"]:
        print(f"  ID={t['id']}, Name={t['name']}, Speciality={t['speciality']}")

def menu_loop():
    """Interactive menu for receptionist and admin actions."""
    load_data()
    print("Welcome to MSMS (Fragments 2.1~2.4)")
    while True:
        print("\n--- Main Menu ---")
        print("1) Check-in a student")
        print("2) Print student card")
        print("3) Update a teacher")
        print("4) Remove a student")
        print("5) List students (view only)")
        print("6) List teachers (view only)")
        print("0) Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # Check-in
            _list_students()
            sid = _input_int("Enter student ID: ")
            course = input("Enter course name (e.g., 'Guitar 101'): ").strip()
            if not course:
                print("Course name cannot be empty.")
                continue
            check_in(sid, course)
            save_data()  # persist immediately

        elif choice == "2":
            # Print student card
            _list_students()
            sid = _input_int("Enter student ID: ")
            try:
                path = print_student_card(sid)
                print(f"Student card created at: {path}")
            except ValueError as e:
                print(str(e))
            # no data mutation, no save needed

        elif choice == "3":
            # Update teacher
            _list_teachers()
            tid = _input_int("Enter teacher ID: ")
            print("Leave a field blank to skip updating it.")
            new_name = input("New name: ").strip()
            new_spec = input("New speciality: ").strip()

            payload = {}
            if new_name:
                payload["name"] = new_name
            if new_spec:
                payload["speciality"] = new_spec

            if not payload:
                print("Nothing to update.")
            else:
                ok = update_teacher(tid, **payload)
                if ok:
                    save_data()  # persist immediately

        elif choice == "4":
            # Remove student
            _list_students()
            sid = _input_int("Enter student ID to remove: ")
            if remove_student(sid):
                save_data()  # persist immediately

        elif choice == "5":
            _list_students()

        elif choice == "6":
            _list_teachers()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose again.")

# Keep the module import-friendly; only run CLI when executed as a script
if __name__ == "__main__":
    # Switch to menu_loop() for Fragment 2.4 runtime
    menu_loop()


# --- Temporary entry point (mainly Fragment 2.1 test) ---
if __name__ == "__main__":
    load_data()
    save_data()
