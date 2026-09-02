import json
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        # ... (next_id counters) ...
        # have it later when loading data
        self._load_data()



    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # TODO: Load students, teachers, and courses as before.
                # to extract information from the json file 
                # using data.get() with string keywords to only extract the data we want
                tempStudent = data.get('students')
                tempTeacher = data.get('teachers')
                tempCourses = data.get('courses')
                
                #because we want to store the data as objects, so we call the StudentUser class
                # to convert the data into objects, and store it in the empty list of an instance from the ScheduleManager.
                for student in tempStudent:
                    newStudent =  StudentUser(student["id"], student["name"])
                    
                    #Student user doesnt accept course_id as a parameter, hence we need to assign it to the instance we created from Student class.
                    newStudent.enrolled_course_ids = student["enrolled_course_ids"]
                    self.students.append(newStudent)
                    # we use 'append', to append the each students information to the instance of ScheduleManager
                    
                # like students, we use for loops to turn the extracted information into objects using class TeacherUser 
                # - append it to the empty lists of the instance created using ScheduleManager    
                for teacher in tempTeacher:
                    newTeacher = TeacherUser(teacher['id'], teacher['name'], teacher['speciality'])
                    self.teachers.append(newTeacher)
                    
                #same thing, create an instance using Course and store information from dictionary in there
                # add the two separate data manually, as it is not included in the parameter of the class 'Course'
                for course in tempCourses:
                    newCourse =  Course(course['id'], course['name'], course['instrument'], course['teacher_id'])
                    newCourse.enrolled_student_ids = (course['enrolled_student_ids']) #because both are lists
                    newCourse.lessons = course['lessons'] #both are lists
                    self.courses.append(newCourse)               
                
                
                # system tries to find the current id counter, sets to three if unable to locate any
                # 3 because there are already two students/teachers in the system already.
                # we can always make changes to it later 
                self.next_student_id = data.get('next_student_id', 3) 
                self.next_teacher_id = data.get('next_teacher_id', 3)
                self.next_course_id = data.get('next_course_id', 104)
                self.next_lesson_id =  data.get('next_lesson_id', 4)
                    

                # TODO: Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
                self.attendance_log = data.get("attendance", [])
                
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students], # this converts the object terms back to dictionaries
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            # TODO: Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            # ... (next_id counters) ...
            'next_student_id': self.next_student_id,
            'next_teacher_id': self.next_teacher_id,
            'next_course_id': self.next_course_id,
            'next_lesson_id': self.next_lesson_id
            
        }
        # TODO: Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
            
    
    


    def check_in(self, student_id, course_id):
        import datetime
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        
        # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True
    
    def print_attendance_log(self):
        '''prints all attendance log records'''
        for log in self.attendance_log: # loops through all dictionaries in attendance lists
            print(f"Student ID: {log['student_id']} | Course ID: {log['course_id']} | Time: {log['timestamp']}")
            
    
    
    
    def find_class_on_day(self, day):
        '''an extra function that checks for lessons on a given day'''
        lessonFound = [] #empty list to store information later
        for course in self.courses: #cycles through all the courses in library
            for lesson in course.lessons: # cycles through all the lesson time for each course
                if day.casefold() == lesson['day'].casefold():
                    lessonFound.append(lesson) #append lesson to list if found day matching.
        return lessonFound
    
    
    def switch_course(self, student_id, from_course_id, to_course_id):
        '''Defines a function to switch course for a student'''
        # TODO: Implement the logic to switch a student by calling methods on the manager.
        for student in self.students: #first loops through all students to locate which student to move
            if student.id == student_id:
                validating = True
                
                #added an extra feature to clarify if user entered the correct student ID
                while validating:
                    tempChoice = input(f'Are you trying to change details for {student.name}? (y/n)  ')
                    if tempChoice.casefold() not in ['y', 'n']:
                        print('Invalid input! Please enter a single character.')
                    else:
                        validating = False
                
                
                if tempChoice.casefold() == 'y': #if user confirmed that they are changing the correct students
                    
                    # checks if students is enrolled in the course provided
                    if from_course_id in student.enrolled_course_ids:
                        student.enrolled_course_ids.remove(from_course_id) # removes old course
                        student.enrolled_course_ids.append(to_course_id) # adds new course in student library
                        
                        # prints message 
                        print(f"{student.name} has been changed from {from_course_id} to {to_course_id}!")
                        print(f"They are currently enrolled in: {student.enrolled_course_ids}")
                        
                        for course in self.courses:
                            if course.id == from_course_id:
                                course.enrolled_student_ids.remove(student.id)
                            if course.id == to_course_id:
                                course.enrolled_student_ids.append(student.id)
                    
                        
                        self._save_data() # saves data
                        print('Data has been saved')
                        return
                    
                    # Prints out a message if a student has been found, but they are are not enrolled in the course provided.
                    else:
                        print('No course has been found to be replaced! Please check again.')
                        return
                
                # if user said this wasn't the student they are changing, they will return to the main menu
                else:
                    print('Returning to main menu...')
                    return
                
        # this prints a message if no students has been found.        
        print(f'No student found with student ID {student_id}')

    # TODO: Also implement find_student_by_id and find_course_by_id helper methods.
    
    # loops through teh list of student objects
    # extracts the student ID and compare with given input ID
    # returns the student if student_id found
    def find_student_by_id(self, student_id):
        """A new helper to find one student by their exact ID."""
        # TODO: Loop through student_db. If a student's ID matches student_id, return the student object.
        for student in self.students:
            if student.id == student_id:
                return student
        # TODO: If the loop finishes without finding a match, return None.
        return None
    

    # loops through the list of courses objects
    # extracts the course ID and compare with given input ID
    # returns the curse if course_id found
    def find_course_by_id(self, course_id):
        '''finds courses, return course object'''
        for course in self.courses:
            if course_id == course.id:
                return course
        return None
        
    def find_teacher_by_id(self, teacher_id):
        '''finds teachers using teacher ID, returns teacher object'''
        for teacher in self.teachers:
            if teacher_id == teacher.id:
                return teacher
        return None
        
    # below are method attributes for a complete PST3 
    def list_courses(self):
        for course in self.courses: # creates a for loop for all courses, and prints corresponding parts.
            print('='*10)
            print()
            print(f'Course ID: {course.id}')
            print(f'Course Name: {course.name}')
            print(f'Instrument: {course.instrument}')
            print(f'Teacher ID: {course.teacher_id}')
            print(f'Enrolled Student IDs: {course.enrolled_student_ids}')
            print(f'Lessons: {course.lessons}')
    
    def reg_courses(self):
        '''This is the extra function I coded, which registers new courses for library'''
        name = input('Enter course name: ')
        instrument = input('Enter instrument: ')
        
        # this is to validate teacher ID
        while True:
            teacher_id = input('Enter teacher ID: ')
            try:
                teacher_id = int(teacher_id)
                teacher_exists = False # sets a temp variable which records if a teacher has been found,
                for teacher in self.teachers:  #loops through all the teacher records
                    if teacher.id == teacher_id: # loops through all teacher IDs to try and match
                        teacher_exists = True
                        break
                if not teacher_exists:
                    print(f'No teacher found with ID {teacher_id}.') 
                    continue # loops back to the start, and allow user to input a new teacher ID
                break
            except ValueError:
                print('Teacher ID must be an integer!')
        
        new_course = Course(self.next_course_id, name, instrument, teacher_id)
        self.courses.append(new_course)
        
        print(f'Success: Course "{new_course.name}" (ID: {new_course.id}) has been registered.')
        
        self.next_course_id += 1   # increments the counter so the next course gets a fresh, unused ID
        self._save_data()
        print('Data has been saved')
        
    def course_input(self):
        ''' This function performs course validation, to see if course ID entered by users are valid, and returns a course ID if valid'''
        '''EXTRA helper function created'''
        while True:
            course_id = input('Enter course ID: ')
            try:
                course_id = int(course_id)
                course = self.find_course_by_id(course_id)
                if course is None:
                    print(f'No course found with ID {course_id}. Please check again.')
                    return None # breaks out so user can check for course IDs
                break
            except ValueError:
                print('Course ID must be entered as an integer!')
        return course_id
        
    def reg_lesson(self):
        '''Registers a new lesson for an existing course'''
        
        # allows user to enter a course ID for the lesson
        # validates if course ID exist
        # again out of method if incorrect course ID is listed and ends function straight away
        while True:
            course_id = input('Enter course ID to add a lesson to: ')
            try:
                course_id = int(course_id)
                course = self.find_course_by_id(course_id)
                if course is None:
                    print(f'No course found with ID {course_id}. Please check again.')
                    return # breaks out so user can check for course IDs
                break
            except ValueError:
                print('Course ID must be entered as an integer!')
        
        # validates day
        while True:
            day = input('Enter day (e.g., Monday): ')
            if day.casefold() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
                print('Invalid day entered! Please check again.')
                continue # this loops because its just syntax
            break
        
        start_time = input('Enter start time (eg: 16:00): ')
        room = input('Enter room: ')
        
        new_lesson = {
            'lesson_id': self.next_lesson_id,
            'day': day,
            'start_time': start_time,
            'room': room
        }
        
        course.lessons.append(new_lesson)
        
        print(f'Lesson added to "{course.name}" on {day} at {start_time} in {room}.')
        
        self.next_lesson_id += 1
        self._save_data()
        print('Data has been saved')
        
    def teacher_id_input(self):
        '''Gets teacher ID inputs and validates, returns teacher ID'''
        '''EXTRA helper function created'''
        while True:
            teacher_id = input('Enter teacher ID:   ')
            try: # try to convert input to integers
                teacher_id = int(teacher_id)
                if teacher_id <= 0:
                    print('Please enter a positive integer number!')
                else:
                    teacher_exists = False
                    for teacher in self.teachers:
                        if teacher.id == teacher_id:
                            teacher_exists = True
                            break
                    if not teacher_exists:
                        print(f'No teacher found with ID {teacher_id}. Please check again.')
                        continue
                    return teacher_id
            except ValueError:
                print('Please enter a valid integer value')
        
    def student_id_input(self):
        '''Gets student id input and validates, returns student ID'''
        '''EXTRA helper function created'''
        while True:
            student_id = input('Enter student ID:   ')
            try: # try to convert input to integers
                student_id = int(student_id)
                if student_id <= 0:
                    print('Please enter a positive integer number!')
                else:
                    if self.find_student_by_id(student_id) is None: # checks if there is such student in system
                        print(f'No student found with ID {student_id}. Please check again.')
                    else:
                        return student_id
            except ValueError:
                print('Please enter an integer value.')
        
        
    
    # for students
    
    def reg_students(self):
        ''' A function to register new students into system '''
        name = input('Enter student name:   ')
        course_id = input('Enter course ID, or leave blank:     ') # allow user to enter a course_ids
        try:
            course_id = int(course_id) # first try converting into integers
            course = self.find_course_by_id(course_id)
            if course is None:
                print(f'No course found with ID {course_id}. Please check again.')
                course_id = None
        except ValueError: #if captures an error, that means an incorrect course ID has been given or no ID has been given
            print('Incorrect/No course ID inputted!')
            course_id = None
            
        if course_id == None:
            print('Students will be registered, but no course has been enrolled for this student.')
            newStudent = StudentUser(self.next_student_id, name) #creates a new  object for student
        else:
            newStudent = StudentUser(self.next_student_id, name) #creates a new  object for student
            newStudent.enrolled_course_ids = [course_id]
            course = self.find_course_by_id(course_id) # this appends the student ID into the course
            course.enrolled_student_ids.append(newStudent.id)
            
        self.next_student_id += 1 #updates next student id
        self.students.append(newStudent) 
        self._save_data()
        
    def remove_student(self, student_id):
        """This function removes student from system given a student ID"""
        student = self.find_student_by_id(student_id)
        
        #the if statement activates if no student has been found
        if student is None:
            print(f'Student with ID: {student_id} was not found!')
            return #exits function
        
        self.students.remove(student)
        print(f'Student {student.name} with ID: {student.id} has been removed from the system')
        
        # this is extra function, double checks if user removed the correct student
        while True:
            userinput = input('Did you remove the correct student (Y/N)?: ').casefold()
            if userinput not in ('n', 'y'):
                print('Wrong input, check again')
            else:
                break
        
        if userinput == 'n':
            self.students.append(student)   # undo — put them back
            print(f'{student.name} has been restored.')
            return
        
        # we also need to remove the students from the course lists.
        # this loops the courses that the students are enrolled in
        for course_id in student.enrolled_course_ids:
            course = self.find_course_by_id(course_id)
            if course != None and student.id in course.enrolled_student_ids:
                course.enrolled_student_ids.remove(student.id)
        
        self._save_data()
        print('Data has been saved.')
    
    def enroll_students(self):
        '''enrols student in avaliable courses'''
        student_id = self.student_id_input()
        course_id = self.course_input()
        
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        
        if student == None or course == None: #exits program, so user can check list of courses and students
            return
        
        
        #extra function, checks if students are already enrolled in the course.
        if course_id in student.enrolled_course_ids:
            print(f'{student.name} is already enrolled in {course.name}.')
            return
        student.enrolled_course_ids.append(course_id) # for the student, adds course id into their attribute        
        course.enrolled_student_ids.append(student_id) # add the student id in the course attributes as well
        self._save_data()
        print('Data has been saved.')
        

    def reg_teacher(self):
        '''Registers new teachers in the system'''
        name = input('Enter teachers name   ')
        speciality = input('Enter teachers speciality:  ')
        newTeacher = TeacherUser(self.next_teacher_id, name, speciality)
        self.teachers.append(newTeacher)
        self.next_teacher_id += 1
        self._save_data()
        print('Data has been saved.')
        
    
    
    
    def update_teacher_info(self):
        '''
        Validates user input and updates a teacher's name and speciality.
        
        '''
        
        teacher_id = self.teacher_id_input()  # gains a valid teacher id from user
        teacher = self.find_teacher_by_id(teacher_id) # extracts teacher object using helper function
        print(f'The teacher you are changing is {teacher.name} with speciality {teacher.speciality}')
        
        new_name = input("Enter teacher's updated name (or leave blank to keep current): ")
        new_speciality = input("Enter teacher's updated speciality (or leave blank to keep current): ")
        
        if new_name == '':
            new_name = teacher.name 
        if new_speciality == '':
            new_speciality = teacher.speciality
        
        teacher.name = new_name
        teacher.speciality = new_speciality
        
        self._save_data()
        print(f'Teacher {teacher.id} updated. Name: {teacher.name}, Speciality: {teacher.speciality}')
            
            
    def list_student(self):
        '''lists all students in the data base'''
        for student in self.students: #loops through all students and prints corresponding outputs
            print(f" Name: {student.name} | ID: {student.id} | Enrolled in: {student.enrolled_course_ids} ")

    def list_teachers(self):
        '''List all teachers in the data base'''
        for teacher in self.teachers:
            print(f" Name: {teacher.name} | ID: {teacher.id} | Speciality: {teacher.speciality} ")       