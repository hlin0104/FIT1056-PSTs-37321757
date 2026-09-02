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
            print()          
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
            print('1. Lists lessons for a certain day.')
            print('2. List courses available.')
            print('3. Register a new course for the system')
            print('4. Register a new lesson for an existing course')
            print(f'='*10)
            print('Options for students')
            print('5. Register a new student')
            print('6. Remove a current student from system')
            print('7. Enroll a student into a course')
            print('8. Switch course for a student')
            print('9. List all current students')
            # note: there are no update student info because I thought switching courses does tha already
            print(f'='*10)
            print('Options for teachers')
            print('10. Register for a teacher')
            print('11. Update Teacher info')
            print('12. List all current teachers')
            print(f'='*10)
            print('Options for attendance')
            print('13. Check in for student')
            print('14. Print all student attendance log')
            print('q. exiting program')
            print()
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
                student_id = manager.student_id_input()
                print('Enter your course that the student is leaving!')
                from_course_id = manager.course_input()
                if from_course_id is None:
                    print('Exiting to main program...')
                    continue 
                #exits program immediately if user enters incorrect courses IDs
                # this was designed on purpose because this allows users to go list out all the courses by choosing the other functions.
                # so the user doesnt have to guess what courses there are
                
                student = manager.find_student_by_id(student_id)
                if from_course_id not in student.enrolled_course_ids:
                    print(f'Student is not enrolled in {from_course_id}!')
                    print('Exiting to main program...')
                    continue
                
                print('Enter your course that the student is joining!')
                to_course_id = manager.course_input()
                if to_course_id is None:
                    print('Exiting to main program...')
                    continue
                
                if to_course_id  in student.enrolled_course_ids:
                    print(f'Student is aleady enrolled in {to_course_id}!')
                    print('Exiting to main program...')
                    continue
                manager.switch_course(student_id, from_course_id, to_course_id)
                
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