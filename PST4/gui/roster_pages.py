# gui/roster_pages.py
import streamlit as st
import pandas as pd

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster")

    # --- View Roster Section (remains the same) ---
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    # ... (code to display the dataframe) ...
    # To make this user-friendly, we should populate the dropdowns dynamically.
    # Get lists of student names and course names from the manager.
    student_list = manager.student_list()
    course_list_dependent_on_day = manager.find_course_on_day(day)
    if course_list_dependent_on_day == None:
        st.write(f'No courses running on {day}')
    else:

        
        # --- Student Check-in Section (now works correctly) ---
        st.subheader("Student Check-in")
        with st.form("check_in_form"):
            
            # these creates selected boxes for the users to choose
            # the lambda function creates the formatting of how the options will be displayed to the UI
            selected_student = st.selectbox("Select Student", student_list, format_func= lambda item: f'{item[0]} with ID: {item[1]}')
            selected_course = st.selectbox("Select Course", course_list_dependent_on_day, format_func= lambda i: i.name)
            
            #this detects whether if the button is pressed
            # the button isnt allowed to be pressed unless a student and a course has been selected
            submitted = st.form_submit_button("Check-in Student", disabled= not selected_course or not selected_student)

            
            if submitted:
                # Convert the selected names back to IDs
                student_id = selected_student[1]
                course_id = selected_course.id

                # This call now works because we implemented the method in PST3.
                success = manager.check_in(student_id, course_id)

                if success:
                    st.success(f"Checked in {selected_student[0]} for {selected_course.name}!")
                else:
                    # The manager's print statements will go to the console, but we can add a GUI error too.
                    st.error("Check-in failed. See console for details. (Is the student enrolled in that course?)")