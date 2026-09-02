# main.py - The View Layer
from app.schedule import ScheduleManager

# FUNCTIONS FOR COURSES AND LESSONS
def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""           
        
    print(f"\n--- Daily Roster for {day} ---")
    # Notice: This code does not need to change. It doesn't care where the Course class lives.
    # It only talks to the manager.
    # TODO: Call a method on the manager to get the day's lessons and print them.
    lessonsFound = manager.find_class_on_day(day)
    
    #extra feature
    #prints out error message if no lessons had been found
    if len(lessonsFound) == 0:
        print(f'No lessons found on {day}!')
    else:
        for lesson in lessonsFound:
            print(f"Lesson ID: {lesson['lesson_id']}" )
            print(f"Lesson Start Time: {lesson['start_time']}")
            print(f"Lesson Location: {lesson['room']}")            
    pass



    

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    runProgram = True
    try: 
        while runProgram:
            print("\n===== MSMS v3 (Object-Oriented) =====")
            # TODO: Create a menu for the new PST3 functions.
            print('Options for COURSES and LESSONS')
            print(f'='*10)
            print('\n\n')
            print('1. Lists lessons for a certain day.')
            print('2. List courses available.')
            print('3. Register a new course for the system')
            print('4. Register a new lesson for an existing course')
            print(f'='*10)
            print('\n\n')
            print('Options for students')
            print('5. Register a new student')
            print('6. Remove a current student from system')
            print('7. Enroll a student into a course')
            print('8. Switch course for a student')
            print('9. List all current students')
            # note: there are no update student info because I thought switching courses does tha already
            print(f'='*10)
            print('\n\n')
            print('Options for teachers')
            print('10. Register for a teacher')
            print('11. Update Teacher info')
            print('12. List all current teachers')
            print(f'='*10)
            print('Options for attendance')
            print('13. Check in for student')
            print('14. Print all student attendance log')
            # Get user input and call the appropriate view function, passing 'manager' to it.
            choice = input("Enter choice: ")
            if choice == '1':
                while True:
                    day = input("Enter day (e.g., Monday): ")
                    if day.casefold() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
                        print('Invalid input! Try again!')
                    else:
                        front_desk_daily_roster(manager, day)
                        break
            
            elif choice == '2':
                manager.list_courses()
                
            elif choice == '3':
                manager.reg_courses()
                
            elif choice =='4':
                manager.reg_lesson()
                
            elif choice == '5':
                manager.reg_students()
                
            elif choice == '6':
                student_id = manager.student_id_input()
                manager.remove_student(student_id)
                
            elif choice == '7':
                manager.enroll_students()
            
            elif choice == '8':
                # this I coded the input validation in main, because I coded this before all the PST2 functions
                # and i only decided I can do my input validations in my method attributes 
                # so I can make my main much much cleaner
                '''coded with input validation as an extra feature'''
                exit = False #a temp variable that tracks if user has entered an incorrect integer course ID
                validating1 = True #validates if student ID is valid
                validating2 = True #validates if from course id is valid
                validating3 = True #validates if to course id is valid
                
                while validating1: # this entire while loop validates input for student IDs
                    student_id = input('Enter student ID:   ')
                    try:
                        student_id = int(student_id)
                        if manager.find_student_by_id(student_id) == None:
                            print(f'No students found with ID {student_id}')
                            exit = True #
                            break
                        
                        validating1 = False
                        break    
                
                    except ValueError:
                        print('Invalid student ID entered! Please enter student ID as an integer!')
                if exit == True: #if user entered an incorrect course ID, exits back to main menu
                    continue
                        
                
                # intentionally designed for input validation to be this way
                # because if user enters wrong course IDs, I thought it would be better for them to exit to main page of program
                # and checks the course ID that the student is enrolled in first, then call this function again
                # but there is still a while loop to check if user had correctly entered integers.
                while validating2:
                    try:
                        from_course_id = input('Enter the course that the student is leaving.   ')
                        from_course_id = int(from_course_id)
                        if manager.find_course_by_id(from_course_id) == None:
                            print('Invalid course ID entered!')
                            exit = True
                            break
                        validating2 = False
                        break
                    except ValueError:
                        print('Course IDs has to be entered as integers!')
                if exit == True:
                    continue
                
                while validating3:
                    try:
                        to_course_id = input('Enter the course that the student is entering.    ')
                        to_course_id = int(to_course_id)
                        if manager.find_course_by_id(to_course_id) == None:
                            print('Invalid course ID entered!')
                            exit = True
                            break
                        validating3 = False
                        manager.switch_course(student_id, from_course_id, to_course_id)
                        break
                    
                    except ValueError:
                        print('Course IDs has to be entered as integers!')
                if exit == True:
                    continue
                
            elif choice == '9':
                manager.list_student()
                
            elif choice == '10':
                manager.reg_teacher()
                
            elif choice == '11':
                manager.update_teacher_info()
                
            elif choice == '12':
                manager.list_teachers()
                
            elif choice == '13':
                student_id = manager.student_id_input()
                course_id = manager.course_input()
                manager.check_in(student_id, course_id)
                
            elif choice == '14':
                manager.print_attendance_log()
                    
            elif choice.lower() == 'q':
                print('Exiting program!')
                break   
            
            else:
                print('Invalid input! Please try again!')
    except KeyboardInterrupt:
        print('Exiting program')
        return
if __name__ == "__main__":
    main()