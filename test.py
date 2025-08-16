from pst2_main import (
    load_data, save_data,
    add_teacher, update_teacher, remove_teacher,
    add_student, update_student, remove_student,
    app_data
)

print("=== START TEST (CRUD) ===")
load_data()
print("After load_data():", app_data)

# Add
t = add_teacher("Alice", "Piano")
s = add_student("Bob", ["Piano 101"])
print("After add:", app_data)

# Update
update_teacher(t["id"], speciality="Advanced Piano")
update_student(s["id"], enrolled_in=["Piano 101", "Theory A"])
print("After update:", app_data)

# Persist
save_data()

# Remove
removed_t = remove_teacher(t["id"])
removed_s = remove_student(s["id"])
print("Removed flags:", removed_t, removed_s)
print("After remove:", app_data)

# Persist again
save_data()
print("=== END TEST ===")
