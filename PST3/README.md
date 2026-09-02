# MSMS v3 (Music School Management System) - Object-Oriented Version

This is my PST3 submission for MSMS. From PST2 to PST3, instead of storing everything as  dictionaries like before, all the data (students, teachers, courses) are now converted into actual objects (StudentUser, TeacherUser, Course), and functions have been refactored.

## How it's structured

Like the requirements, this was separated into view/Model files. With 4 model files, and 1 view file.

main.py - this is the View layer. It only handles user interaction (printing menus, taking input, validating input for some) and does most of the logic to the Class ScheduleManager. Most of the time is just calls method attributes on manager(the instance we created using class ScheduleManager), and then the method attributes will perform the logic and does whichever was requested.

schedule.py - this is the Model/Controller. ScheduleManager owns all the data and all the logic accessed from method attributes.

student.py, teacher.py, user.py - the classes. StudentUser and TeacherUser both inherit from a base User class, since they share id and name. Course is its own separate class since it doesn't really share the same parameters as 'blue prints' like the other two
msms.json - where everything actually gets saved/loaded from.

Only one ScheduleManager instance ever gets created as soon as main() is run, and it gets passed around to every function that needs it. This way there's one single source of data instead of multiple copies floating around that could get out of sync.

## Menu Options

### Courses & Lessons

List lessons for a certain day
List all courses
Register a new course
Register a new lesson for an existing course

### Students 
Register a new student 
Remove a current student 
Enroll a student into a course 
Switch course for a student 
List all current students

(Note: there's no separate "update student info" option, since switching courses already covers the main thing you'd want to update for a student)

### Teachers 
Register a new teacher 
Update teacher info 
List all current teachers

### Attendance
Check in a student 
Print the full attendance log

Extra features I added

A few things beyond the base requirements that I thought were worth adding to make it more complete / I added to help with other codes

**Input validation everywhere**** - basically every input in this program (student IDs, course IDs, teacher IDs, days) gets validated with a loop so the program doesn't crash on bad input, it just asks again.

**Confirmation prompts** - for things like switch_course and remove_student, the program double checks with the user (y/n) before actually doing the change, in case they entered the wrong ID by accident. remove_student even lets you undo the removal if you say "n".

**Helper validator methods** - student_id_input(), course_input(), and teacher_id_input() are all reusable methods that prompt + validate + return an ID, so I'm not rewriting the same validation loop in all different places.

**Duplicate enrollment check** - enroll_students() method attributes checks if a student is already enrolled in a course before adding them again, so you don't end up with duplicate entries.

**Two-way syncing** - whenever a student gets enrolled/removed/switched from a course, both sides get updated (the student's enrolled_course_ids list AND the course's enrolled_student_ids list), so the data doesn't end up contradicting itself.

A note on design decisions

For switch_course, if the user enters a student ID that doesn't exist, it loops back and asks again (since that's usually just a typo). But if they enter a course ID that isn't registered in the system, I made it exit back to the main menu instead of looping - since if the course ID they entered doesn't exist, retrying and guessing the for a valid course ID over and over isn't going to help. They'd need to go check the course list first, then come back and try again.

