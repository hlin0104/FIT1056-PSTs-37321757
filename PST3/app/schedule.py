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
        
