# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Search Section (remains the same) ---
    st.subheader("Find a Student")
    
    #asks the user if they wanna find students by entering a name or an id
    temp_choice = st.selectbox("Find student by", ['id', 'name'])
    
    # creates a form that covers the number/ text inputs, so it clears once submitted to prevent double clicking
    with st.form('find students', clear_on_submit=True):
        if temp_choice == 'id':
            # extra feature i added, where the user can just adjust the id without retyping
            requested_id = st.number_input('Enter the Student ID', min_value=1, step=1) 
        else:
            requested_name =  st.text_input("Enter the Student Name")
            requested_name = requested_name.strip() #stripping it to prevent unwanted space
        #creating that button
        search = st.form_submit_button('Search')
        
        # if they pressed the button and chose ID as method of searching
        if search and temp_choice == 'id':
            student = st.session_state.manager.find_student_by_id(requested_id)
            if student == None:
                st.warning(f'No student has been found with ID: {requested_id}')
            else:
                st.write(f'Name: {student.name}')
                st.write(f'Id: {student.id}')
                st.write(f'Enrolled in Courses {student.enrolled_course_ids}')
                
        # if they pressed the button and chose name as method of searching
        # I couldn't combine these two because they have different error messages
        elif search and temp_choice == 'name':
                student_list = st.session_state.manager.find_student_by_name(requested_name)
                if student_list == None:
                    st.warning(f'No student has been found with name: {requested_name}, please check spelling!')
                else:
                    for student in student_list:
                        st.write(f'Name: {student.name}')
                        st.write(f'Id: {student.id}')
                        st.write(f'Enrolled in Courses {student.enrolled_course_ids}')

            

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New Student")
    
    #again, creating a form so it clears once submitted 
    with st.form("registration_form", clear_on_submit=True):
        reg_name = st.text_input("New Student Name")
        
        #instead of instrument I changed it to course, because an instrument can have different courses, such as beginner and intermediate
        reg_course = st.selectbox("First Course", st.session_state.manager.course_name_list())
        submitted = st.form_submit_button("Register Student")
        
        if submitted:
            # This call now works because we implemented the method in PST3.
            # TODO: Add a check for blank name/instrument.
            if reg_name == '' or reg_name.isdigit():
                st.warning("Please enter a valid name, that's not empty nor a number!")
            elif reg_name and reg_course: 
                new_student = manager.register_new_student(reg_name, reg_course)
                if new_student:
                    st.success(f"Successfully registered {reg_name}!")
                    st.balloons()
                else:
                    st.error(f"Could not register student. A teacher for {reg_course} might not be available.")
            else:
                st.warning("Please enter both a name and an instrument.")