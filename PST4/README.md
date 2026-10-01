

# MSMS v4 (Music School Management System) - Streamlit GUI Version

This is my PST4 submission for MSMS. From PST3 to PST4, the main change is adding a graphical interface using Streamlit, so the user can interact with the system through a browser using forms, dropdown boxes and buttons.

The program still uses the objects from PST3, including StudentUser, TeacherUser and Course. ScheduleManager handles the data and the logic, while the GUI calls its methods and displays the results, note the GUI haven't included every feature from PST3.

## How to run

python -m streamlit run main.py


The program loads its data from `data/msms.json`, so the terminal needs to be inside PST4 when running this command. The supplied JSON file needs to be present.

## How it's structured

main.py - this is the launcher. Its only job is to call launch() from the main dashboard and start the GUI.

gui/main_dashboard.py - sets the browser tab title, uses a wide page layout and creates the sidebar navigation. It decides which page to show depending on what the user selects.

gui/student_pages.py - handles searching for students and registering new students. It collects the user's input, calls the manager and displays the results or warning messages.

gui/roster_pages.py - lets the user select a weekday and filters the courses available for check-in. It also contains the student check-in form.

app/schedule.py - this is the Model/Controller. ScheduleManager stores the student, teacher and course objects, performs the main logic, and loads/saves the data.

app/student.py, app/teacher.py, app/user.py - these contain the classes. StudentUser and TeacherUser inherit from User because both have an ID and name. Course is a separate class, and stores its instrument, teacher ID, enrolled students and lessons.

data/msms.json - this is where every data is saved


## Student Management

### Finding a student

The user first chooses whether they wanna search using a student ID or a name.

Searching by ID uses a number input with a minimum value of 1. The manager returns the student with that ID, or None if there isn't a matching student.

Searching by name uses a text input. Extra spaces at the start and end of the entered search are removed. The manager compares the full name using `.casefold()`, so the capitalisation doesn't need to be exactly the same.

Name searches return all students with that name. This allows students with duplicate names to still appear separately, since they each have their own ID.

The results display the student's name, ID and enrolled course IDs. If nothing is found, the GUI shows a warning.

### Registering a student

The registration form asks for a new student name and their first course.

I changed the selection from an instrument to a course, because the same instrument can have different courses, such as beginner and intermediate classes.

The form rejects an empty name or a name made entirely of digits. Once submitted, it calls `register_new_student(name, course_name)`.

This method finds the matching course, creates a StudentUser object and updates both sides of the enrolment:

- The course ID is added to the student's enrolled_course_ids.
- The student ID is added to the course's enrolled_student_ids.

It then adds the student to the manager, increments the next student ID and saves the data. The new student object is returned so the GUI can display a success message and balloons.

Both the search and registration forms use `clear_on_submit=True`. This resets the inputs after submission, including unsuccessful submissions. Clearing the form helps avoid leaving the previous name in the box, but it doesn't prevent someone from entering and registering the same details again.

## Daily Roster and Student Check-in

The user selects a day from Monday to Friday.

The manager checks each course's lessons to find which courses run on that day. Those courses become the options in the check-in dropdown. If no courses are found, the page displays a message saying there are no courses running on the selected day.

For check-in, the user selects a student and a course, then presses the Check-in Student button.

The GUI gets the student's ID from the selected name/ID pair and the course ID from the selected Course object. It passes these to `check_in(student_id, course_id)`.

The manager checks that both records exist and that the student is enrolled in the selected course. If these checks pass, it adds an attendance record containing the student ID, course ID and current timestamp, then saves the data.

The method returns True or False so the GUI can show whether check-in was successful.

The selected weekday filters the course options. The attendance timestamp still records the actual irl time of check-in.

## Extra features I added

A few things I added to make the GUI easier for staff to use:

### 1. Choosing how to search for students

I added a dropdown that lets the user choose between searching by ID or name. This means they can still find a student even if they don't remember the ID.

The name search also displays all matching students instead of stopping at the first one, since different students can have the same name.

### 2. Clearer dropdown formatting for check-in

I used `format_func` to display both the student's name and ID in the dropdown, such as `Alex with ID: 12`.

This makes it easier to tell students apart when their names are duplicated. The course dropdown displays the course name while still keeping the Course object available, so the program can get its ID when checking in.

### 3. Filtering check-in courses based on the selected day

I added `find_course_on_day(day)` to check which courses have lessons on the selected weekday.

The check-in dropdown then only shows those courses. This makes the options more relevant to the day the user is viewing, instead of showing every course in the system.

### 4. Adjusting student IDs without retyping

I used `st.number_input()` for the student ID search, with a minimum of 1 and a step of 1.

The user can type an ID directly, or use the increase/decrease buttons to adjust it one number at a time. This makes it easier to change the ID without deleting and retyping it.