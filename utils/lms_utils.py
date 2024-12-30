import json
import os
from datetime import datetime

# Singleton class to manage Learning Management System data
class LMSManager:
    _instance = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LMSManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initializes the LMSManager by setting up the data file path and loading data."""
        self.data_file = os.path.join(os.getcwd(), "my_lms_data.json")
        print(f"LMS data file path: {self.data_file}")  # Debug print
        self.load_data()

    def load_data(self):
       """Loads LMS data from a JSON file, creates a default structure if the file doesn't exist."""
       try:
           if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    LMSManager._data = json.load(f)
                    print(f"Loaded existing data: {LMSManager._data}")  # Debug print
           else:
                 LMSManager._data = {
                     "courses": [],
                     'users': {},
                     'enrollments': {}
                 }
                 self.save_data()
                 print("Created new data file")  # Debug print
       except Exception as e:
            print(f"Error loading data: {e}")  # Debug print
            LMSManager._data = {
                    'users': {},
                    'courses': {},
                    'enrollments': {}
                }
                

    def save_data(self):
        """Saves the current LMS data to the JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(LMSManager._data, f, indent=2)
            print(f"Saved data: {LMSManager._data}")  # Debug print
        except Exception as e:
            print(f"Error saving data: {e}")  # Debug print

    def create_course(self, course_data):
        """Creates a new course and adds it to the LMS data."""
        try:
            LMSManager._data["courses"].append(course_data)
            print(f"Created course: {course_data['courseTitle']}")  # Debug print
            self.save_data()
            return True
        except Exception as e:
            print(f"Error creating course: {e}")  # Debug print
            return None
    def enroll_user(self, user_id, course_title):
         # Enrolls a user in a specific course and initializes progress tracking
        try:
            course_found = False
            for course in LMSManager._data["courses"]:
                if course["courseTitle"] == course_title:
                    course_found = True
                    break

            if not course_found:
                print(f"Course {course_title} not found")  # Debug print
                return False
            
            if user_id not in LMSManager._data['users']:
                LMSManager._data['users'][user_id] = {
                    'enrolled_courses': [],
                    'progress': {}
                }
           
            if course_title not in LMSManager._data['users'][user_id]['enrolled_courses']:
                LMSManager._data['users'][user_id]['enrolled_courses'].append(course_title)
                LMSManager._data['users'][user_id]['progress'][course_title] = {
                    'status': 'enrolled',
                    'completed_modules': [],
                    'completed_assessments': [],
                    'enrolled_at': datetime.now().isoformat()
                }
                print(f"Enrolled user {user_id} in course {course_title}")  # Debug print
                self.save_data()
            return True
        except Exception as e:
            print(f"Error enrolling user: {e}")  # Debug print
            return False
    def get_user_courses(self, user_id):
        # Retrieves all courses enrolled by a specific user with their progress
        try:
            print(f"Getting courses for user {user_id}")  # Debug print
            print(f"Current data: {LMSManager._data}")  # Debug print
            
            if user_id not in LMSManager._data['users']:
                print(f"User {user_id} not found in {LMSManager._data['users'].keys()}")  # Debug print
                return []
            
            courses = []
            for course_title in LMSManager._data['users'][user_id]['enrolled_courses']:
                 for course in LMSManager._data["courses"]:
                     if course["courseTitle"] == course_title:
                        progress = LMSManager._data['users'][user_id]['progress'].get(course_title, {})
                        courses.append({
                            'course_title': course_title,
                            'name': course.get('courseTitle'),
                            'description': course.get('description'),
                            'status': progress.get('status'),
                            'enrolled_at': progress.get('enrolled_at'),
                             'completed_modules': progress.get('completed_modules'),
                             'completed_assessments':progress.get('completed_assessments')
                        })
            print(f"Found courses: {courses}")  # Debug print
            return courses
        except Exception as e:
            print(f"Error getting user courses: {e}")  # Debug print
            return []
    
    def get_course_details(self, course_title):
        # Retrieves course details based on the course title
       try:
           print(f"Getting details for course: {course_title}")
           for course in LMSManager._data["courses"]:
                if course.get("courseTitle") == course_title:
                    print(f"Found Course: {course}")
                    return course
           print(f"Course not found {course_title}")
           return None
       except Exception as e:
            print(f"Error getting course details: {e}")
            return None
    
    def mark_module_completed(self, user_id, course_title, module_title):
        # Marks the module as completed
         try:
            if user_id not in LMSManager._data['users']:
                print(f"User {user_id} not found")
                return False

            if course_title not in LMSManager._data['users'][user_id]['enrolled_courses']:
                print(f"User {user_id} is not enrolled in the {course_title} course.")
                return False
                
            progress = LMSManager._data['users'][user_id]['progress'].get(course_title)
            if progress:
                if module_title not in progress['completed_modules']:
                    progress['completed_modules'].append(module_title)
                    self.save_data()
                    print(f"Module {module_title} marked as completed for user {user_id} in course {course_title}")
                    return True
                else:
                    print(f"Module {module_title} already marked as completed for user {user_id} in course {course_title}")
                    return True
            else:
              print(f"Progress not found for user {user_id} in course {course_title}")
              return False

         except Exception as e:
            print(f"Error marking module as completed: {e}")
            return False
    
    def mark_assessment_completed(self, user_id, course_title, assessment_description):
      #Marks the assessment as completed
         try:
            if user_id not in LMSManager._data['users']:
                print(f"User {user_id} not found")
                return False

            if course_title not in LMSManager._data['users'][user_id]['enrolled_courses']:
                print(f"User {user_id} is not enrolled in the {course_title} course.")
                return False
                
            progress = LMSManager._data['users'][user_id]['progress'].get(course_title)
            if progress:
                if assessment_description not in progress['completed_assessments']:
                    progress['completed_assessments'].append(assessment_description)
                    self.save_data()
                    print(f"Assessment {assessment_description} marked as completed for user {user_id} in course {course_title}")
                    return True
                else:
                   print(f"Assessment {assessment_description} already marked as completed for user {user_id} in course {course_title}")
                   return True
            else:
              print(f"Progress not found for user {user_id} in course {course_title}")
              return False

         except Exception as e:
            print(f"Error marking assessment as completed: {e}")
            return False