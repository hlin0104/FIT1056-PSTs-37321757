# MSMS v2 — Persistent Music School Management System

An application for managing students, teachers, and class
attendance at a music school. Data is kept in memory in a single global
dictionary while the program runs, and is loaded from / saved to a JSON
file locally so records persist between sessions!

## Requirements

- **Python 3.14 or above is required. 
- No third-party packages are needed — only the standard library
  (`json`, `datetime`).

## Data Storage

- All data is stored in the dictionary named `app_data`
- On exit (or after any change), `app_data` is recorded to a JSON file
  (`msms.json` by default) via `save_data()`
- On startup, `load_data()` reads `msms.json` back into `app_data`. If the
  file doesn't exist yet, a fresh default structure is created with empty
  `students`, `teachers`, and `attendance` lists, and ID counters
  (`next_student_id`, `next_teacher_id`) starting at `1`.
- Records are stored as _dictionaries inside lists_ (not custom
  classes), e.g. `app_data["students"]` is a list of
  `{"id": ..., "name": ..., "enrolled_in": ...}` dictionaries.

## Functions

### Persistence
- **`load_data(path=DATA_FILE)`** — Loads `app_data` from a JSON file, or
  initializes a default empty structure if the file is missing.
- **`save_data(path=DATA_FILE)`** — Writes the current `app_data` to a
  JSON file.

### Core CRUD
- **`add_teacher(name, speciality)`** — Creates a teacher record with an
  auto-incremented ID and appends it to `app_data["teachers"]`.
- **`update_teacher(teacher_id, **fields)`** — Finds a teacher by ID and
  merges the given keyword fields into their record.
- **`update_student(student_id, **fields)`** — Finds a student by ID and
  merges the given keyword fields into their record.
- **`remove_student(student_id)`** — Removes a student record from the
  system (see Extra Features below for the full behaviour).
- **`remove_teacher(teacher_id)`** — Removes a teacher record from the
  system (see Extra Features below for the full behaviour).

### Front Desk
- **`teacher_register(name, speciality)`** — Registers a new teacher with
  an auto-incremented ID.
- **`front_desk_register(name, instrument)`** — Registers a new student
  and, if an instrument is provided, enrolls them in it.
- **`find_student_by_id(student_id)`** — Helper that searches
  `app_data["students"]` for a matching ID and returns the record (or
  `None`).
- **`front_desk_enrol(student_id, instrument)`** — Enrolls an existing
  student (found via `find_student_by_id`) in a given instrument/course.

### Receptionist
- **`check_in(student_id, course_id, timestamp=None)`** — Records a
  student's attendance for a course, timestamped with the current time by
  default.

### Reporting / Output
- **`print_student_card(student_id)`** — Writes a text-file "ID badge" for
  a student (`{student_id}_card.txt`) containing their ID, name, and
  enrolled instrument(s).
- **`print_student_list()`** — Prints all students and their details to
  the console.
- **`print_teacher_list()`** — Prints all teachers and their details to
  the console.

### Application Entry Point
- **`main()`** — Runs the interactive menu loop: loads data on startup,
  presents numbered options (check-in, print card, update/remove
  teacher or student, register student/teacher, list students/teachers,
  quit), validates user input for each option, and saves data after any
  change (plus a final save on exit).

## Extra Features

These are enhancements beyond the base `TODO` requirements, as called out
in the functions' own docstrings:

- **`remove_student(student_id)`**
  - Validates that the student ID exists before removing.
  - Asks for confirmation ("Did you remove the correct student?") after
    removal, with input validation restricted to Y/N.
  - If the answer is "N", reverts the removal by re-inserting the
    student at their original position.
  - If confirmed, re-numbers the IDs of all remaining students so they
    stay in ascending order with no gaps, and decrements
    `next_student_id` accordingly.

- **`remove_teacher(teacher_id)`**
  - Same confirmation-and-revert workflow as `remove_student`, applied to
    teachers: validates the ID, asks for Y/N confirmation, reverts on
    "N", and re-numbers remaining teacher IDs in ascending order on
    confirmation (decrementing `next_teacher_id`).

- **`check_in(student_id, course_id, timestamp=None)`**
  - Validates that the student ID actually exists before logging
    attendance.
  - Prints a confirmation message that includes the student's name (not
    just their ID) when check-in succeeds, and a clear error message if
    the ID isn't found.

- **Teacher update flow**
  - Prints a confirmation line showing the teacher's *current* name and
    speciality before making changes, so the user can verify they're
    editing the right record.
  - Lets the user leave either field blank to keep its existing value,
    rather than forcing them to re-enter both fields every time.

- **Student update flow**
  - Same pattern as the teacher update flow: shows the student's current
    name and enrolled instrument for confirmation, and allows blank
    input to preserve the existing value for name or instrument.

- **Input validation loops**
  - All menu options that require a student or teacher ID loop until the
    user enters a valid positive integer, catching non-numeric input and
    zero/negative values with clear error messages before proceeding.