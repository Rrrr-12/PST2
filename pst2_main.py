# pst2_main.py - The Persistent Application (Fragment 2.1)
import json
import datetime  # will be used in later fragments

DATA_FILE = "msms.json"
app_data = {}  # global dictionary holding all application data

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Load all application data from a JSON file. 
    If the file does not exist, initialize with default structure."""
    global app_data
    try:
        with open(path, 'r', encoding='utf-8') as f:
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Save all application data to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(app_data, f, indent=4, ensure_ascii=False)
    print("Data saved successfully.")

# temporary entry point for testing Fragment 2.1
if __name__ == "__main__":
    load_data()      
    save_data()      

