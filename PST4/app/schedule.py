import json
from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.next_lesson_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # The logic here remains the same, but the source of the Course class has changed.
                tempStudent = data.get('students')
                tempTeacher = data.get('teachers')
                tempCourses = data.get('courses')
                
                # TODO: For each dictionary in data['students'], create a StudentUser object and append to self.students.
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
                
                # TODO: Do the same for teachers (creating TeacherUser objects).
                for teacher in tempTeacher:
                    newTeacher = TeacherUser(teacher['id'], teacher['name'], teacher['speciality'])
                    self.teachers.append(newTeacher)
                    
                #same thing, create an instance using Course and store information from dictionary in there
                # add the two separate data manually, as it is not included in the parameter of the class 'Course'
                # TODO: Do the same for courses (creating Course objects).
                for course in tempCourses:
                    newCourse =  Course(course['id'], course['name'], course['instrument'], course['teacher_id'])
                    newCourse.enrolled_student_ids = (course['enrolled_student_ids']) #because both are lists
                    newCourse.lessons = course['lessons'] #both are lists
                    self.courses.append(newCourse)  

                # system tries to find the current id counter, sets to three if unable to locate any
                # 3 because there are already two students/teachers in the system already.

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
        # The logic here remains the same.
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
        "students": [s.__dict__ for s in self.students], # this converts the object terms back to dictionaries
        "teachers": [t.__dict__ for t in self.teachers], # but it doesnt convert pure strings, 
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
            