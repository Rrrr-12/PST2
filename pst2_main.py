# pst2_main.py - The Persistent Application (Fragment 2.1)
import json
import datetime  # will be used in later fragments

DATA_FILE = "msms.json"
app_data = {}  # global dictionary holding all application data

# --- Core Persistence Engine ---
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

# temporary entry point for testing Fragment 2.1
if __name__ == "__main__":
    load_data()      
    save_data()      


