
MSMS.py is a simple Python front desk system for a music school. It manages basic student and teacher records in memory and provides a text menu for registering students, enrolling instruments, and searching records.

What the system does:
- Stores student records with ID, name, and enrolled instruments.
- Stores teacher records with ID, name, and speciality.
- Lets the user register a new student and immediately enrol them in an instrument.
- Lets the user enrol an existing student in an additional instrument.
- Lets the user search for students and teachers by name or speciality.
- Lets the user list all students or teachers.
- Includes an extra lookup for students enrolled in a specific instrument.

Major parts / function responsibilities:
- `Student` class: holds `id`, `name`, and `enrolled_in` instrument list.
- `Teacher` class: holds `id`, `name`, and `speciality`.
- `student_db` and `teacher_db`: in-memory lists that store the current records.
- `add_teacher()`: creates a new teacher and appends it to `teacher_db`.
- `list_students()` / `list_teachers()`: print the current student or teacher records.
- `find_students()` / `find_teachers()`: search the in-memory lists for matching names or specialities.
- `find_student_by_id()`: helper used to locate a student by exact ID.
- `front_desk_register()`: registers a new student and enrols them in the requested instrument.
- `front_desk_enrol()`: enrols an existing student in another instrument.
- `front_desk_lookup()`: performs a combined student and teacher search.
- `find_student_instrument()`: finds students enrolled in a specific instrument.
- `main()`: runs the interactive menu loop and handles user input.

How to run the program:
1. Open a terminal in the `PST1/msms-project` folder.
2. Activate Python if required.
3. Run `python MSMS.py`.
4. Use the menu options by entering the number of the desired action, or `q` to quit.

How to test it:
- Start the program and choose option `1` to register a new student.
- Choose option `2` to enrol an existing student by ID.
- Choose option `3` to search for student or teacher names.
- Choose option `4` or `5` to list all students or teachers.
- Choose option `6` and enter an instrument name to find students enrolled in that instrument.

Assumptions, design choices, and extensions:
- Data is kept in memory only, so all records reset when the program exits.
- The program uses incremental integer IDs for students and teachers.
- Search operations are case-insensitive for easier matching.
- An extension was added to look up students by enrolled instrument.
- The project is intended for Python 3.10 or newer.
- No persistent file storage is included, so this is a temporary demo system rather than a production database-backed application.

AI DECLARATION: I've used AI(gemini) at the last to check for any syntax error that existed in my code, I also fed it my README file to check for syntax and format options.