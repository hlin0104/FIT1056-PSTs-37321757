# pst2_main.py - The Persistent Application

import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            # TODO: Use json.load(f) to load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # TODO: If the file doesn't exist, initialize 'app_data' with a default dictionary.
        # It should have keys like: "students", "teachers", "attendance", "next_student_id", "next_teacher_id".
        # The lists should be empty and the IDs should start at 1.
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # TODO: Open the file at 'path' in write mode ('w').
    # Use json.dump() to write the global 'app_data' dictionary to the file.
    # Use the 'indent=4' argument in json.dump() to make the file readable.
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")
    
    
# --- Full CRUD for Core Data ---
# Note: We are now working with lists of dictionaries, not lists of objects.

def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    # TODO: Get the next teacher ID from app_data['next_teacher_id'].
    teacher_id = app_data['next_teacher_id']
    # TODO: Create a new teacher dictionary with 'id', 'name', and 'speciality' keys.
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    # TODO: Append the new dictionary to the app_data['teachers'] list.
    app_data['teachers'].append(new_teacher)
    # TODO: Increment the 'next_teacher_id' in app_data.
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    # TODO: Loop through the app_data['teachers'] list.
    for teacher in app_data['teachers']:
        # TODO: If a teacher's 'id' matches teacher_id:
        if teacher['id'] == teacher_id:
            # Use the .update() method on the teacher dictionary to apply the 'fields'.
            # the update is a built in function for dictionaries, field is an argument input with a keyword for a dictionary and value
            # the update function basically changes a value if keyword u entered was in the dictionary already
            # otherwise it just adds a new keyword to that dictionary 
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")
    
def update_student(student_id, **fields):
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f'Error: Student with ID {student_id} not found.')

def remove_student(student_id):
    """
    Removes a student from the data store.
    Fixes all student IDs and ensured that they were still in ascending order and not skipping numbers
    """
    # TODO: Find the student dictionary in app_data['students'] with the matching ID.
    for student in app_data["students"]:
        if student_id == student["id"]:
            removed_student = student
            app_data["students"].remove(student)
            print(f'Student {student["name"]} with {student["id"]} has been removed from the system')
            while True:
                userinput = input('Did you remove the correct student(Y/N)?:    ').casefold()
                if userinput not in ('n', 'y'):
                    print(f'Wrong inputs, check again')
                else:
                    break
            if userinput =='n':
                app_data["students"].insert(removed_student["id"]-1, removed_student)
            else:
                for student in app_data["students"]:
                    if student["id"] > removed_student["id"]:
                        student["id"] -= 1
                app_data["next_student_id"] -= 1
        return 
    print(f'Student with ID: {student_id} was not found!')
                
            
def remove_teacher(teacher_id):
    '''
    
    removes teacher from system with specified teacher id
    sorts teachers id as well in order
    
    '''
    for teacher in app_data["teachers"]:
        if teacher_id == teacher["id"]:
            removed_teacher = teacher
            app_data["teachers"].remove(removed_teacher)
            print(f"Teacher {removed_teacher["name"]} with ID: {removed_teacher["id"]} was removed from the system.")
            while True:
                userinput = input('Did you remove the correct teacher(Y/N)?:    ').casefold()
                if userinput not in ('n', 'y'):
                    print(f'Wrong inputs, check again')
                else:
                    break
            if userinput =='n':
                app_data["teachers"].insert(removed_teacher["id"]-1, removed_teacher)
            else:
                for teacher in app_data["teachers"]:
                    if teacher["id"] > removed_teacher["id"]:
                        teacher["id"] -= 1
                app_data["next_teacher_id"] -= 1
        return
    print(f'Teacher with ID: {teacher_id} was not found!')
        



#moved front desk functions from pst1 and modified so data was stored in lists, rather than objects.
def front_desk_register(name, instrument=None):
    """High-level function to register a new student and enrol them."""
    student_id = app_data["next_student_id"]
    new_student = {"name": name, "id": student_id, "enrolled_in": []}
    app_data["students"].append(new_student)
    app_data["next_student_id"] += 1
    if instrument != None:
        front_desk_enrol(student_id, instrument)
        print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{instrument}'.")
    
def find_student_by_id(student_id):
    """A new helper to find one student by their exact ID."""
    # TODO: Loop through student_db. If a student's ID matches student_id, return the student object.
    for student in app_data["students"]:
        if student["id"] == student_id:
            return student
    # TODO: If the loop finishes without finding a match, return None.
    return None

def front_desk_enrol(student_id, instrument):
    """High-level function to enrol an existing student in a course."""
    # TODO: Use your new find_student_by_id() helper.
    student = find_student_by_id(student_id)
    # TODO: If the student is found, append the instrument to their 'enrolled_in' list.
    if student:
        student['enrolled_in'].append(instrument)
        print(f"Front Desk: Enrolled student {student_id} in '{instrument}'.")
    else:
        # TODO: If the student is not found, print an error message like "Error: Student ID not found."
        print(f"Error: Student ID {student_id} not found.")



# --- New Receptionist Features ---
def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    if timestamp is None:
        # TODO: Get the current time as a string using datetime.datetime.now().isoformat()
        timestamp = datetime.datetime.now().isoformat()
    
    # TODO: Create a check-in record dictionary.
    # It should contain 'student_id', 'course_id', and 'timestamp'.
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    # TODO: Append this new record to the app_data['attendance'] list.
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")




def print_student_card(student_id):
    """Creates a text file badge for a student."""
    # TODO: Find the student dictionary in app_data['students'].
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        # TODO: Create a filename, e.g., f"{student_id}_card.txt".
        filename = f"{student_id}_card.txt"
        # TODO: Open the file in write mode ('w').
        with open(filename, 'w') as f:
            # Write the student's details to the file in a nice format.
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")

