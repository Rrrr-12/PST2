from pst2_main import (
    load_data, save_data,
    add_teacher, update_teacher, remove_teacher,
    add_student, update_student, remove_student,
    check_in, print_student_card,
    app_data
)

# --- Fragment 2.2 quick test (CRUD) ---
print("=== START TEST (CRUD) ===")
load_data()
print("After load_data():", app_data)

# Create sample teacher and student
t = add_teacher("Alice", "Piano")
s = add_student("Bob", ["Piano 101"])
print("After add:", app_data)

# Update records
update_teacher(t["id"], speciality="Advanced Piano")
update_student(s["id"], enrolled_in=["Piano 101", "Theory A"])
print("After update:", app_data)

# Persist changes
save_data()

# Remove records and persist again
removed_t = remove_teacher(t["id"])
removed_s = remove_student(s["id"])
print("Removed flags:", removed_t, removed_s)
print("After remove:", app_data)
save_data()
print("=== END TEST ===")

# --- Fragment 2.3 quick test ---
print("=== START TEST (2.3) ===")
load_data()

# Ensure we have at least one student
if not app_data["students"]:
    s = add_student("Charlie", ["Guitar 101"])
else:
    s = app_data["students"][0]

# Check-in and persist
check_in(s["id"], "Guitar 101")
save_data()

# Print badge
badge_path = print_student_card(s["id"])
print("Badge path:", badge_path)
print("=== END TEST (2.3) ===")
