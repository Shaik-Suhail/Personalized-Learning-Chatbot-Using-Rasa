from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','utils')))
from utils.lms_utils import LMSManager
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class ActionProvideLearningRecommendations(Action):
    # Handles course recommendations and enrollment
    def __init__(self):
        super().__init__()
        self.lms = LMSManager()

    def name(self) -> Text:
        return "action_provide_learning_recommendations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Processes user input and provides personalized course recommendations
        latest_message = tracker.latest_message['text'].lower()
        user_id = tracker.sender_id
        topic = tracker.get_slot("topic")
        logging.debug(f"ActionProvideLearningRecommendations: user_id={user_id}, topic={topic}, message='{latest_message}'")

        # Handle feedback responses
        if any(word in latest_message for word in ['helpful', 'thanks', 'good', 'great']):
            response = "I'm glad you found it helpful! You can type 'show my courses' to see your enrolled courses."
            dispatcher.utter_message(text=response)
            return []

        # Extract experience and interest
        experience = None
        interest = None

        if 'beginner' in latest_message:
            experience = 'beginner'
        elif 'intermediate' in latest_message:
            experience = 'intermediate'

        if  topic:
             interest = topic
        else:
            # Determine the interest area
            if 'web' in latest_message or 'web development' in latest_message :
                interest = 'Web Development'
            elif 'app' in latest_message or 'app development' in latest_message:
                interest = 'App Development'
            elif 'python' in latest_message:
               interest = 'Python'
            elif 'java' in latest_message:
               interest = 'Java'
            elif 'c++' in latest_message or 'cpp' in latest_message:
               interest = 'C++'
            elif 'fullstack' in latest_message or 'full stack' in latest_message:
                interest = 'Full Stack Development'
            elif 'flutter' in latest_message:
                interest = 'Flutter'
        if experience and interest:
            try:
                # Create course name and description
                course_name = f"{interest.title()} for {experience.title()}s"
                description = f"A curated learning path for {experience}s in {interest}"

                # Get course details from the lms
                course_details = self.lms.get_course_details(interest)
                if course_details:
                    # Create course and enroll user
                    logging.debug(f"Creating course for user {user_id}")  # Debug print
                    course_data =  {
                      "courseTitle": course_details['courseTitle'],
                       "description": course_details["description"],
                       "syllabus": course_details.get("syllabus", []),
                       "progressTracking": course_details.get("progressTracking", [])
                   }
                    self.lms.create_course(course_data)

                    if course_title := course_details.get("courseTitle"):
                        logging.debug(f"Enrolling user {user_id} in course {course_title}")  # Debug print
                        self.lms.enroll_user(user_id, course_title)

                        response = f"🎉 Welcome to {course_name}!\n\n"
                        response += "I've enrolled you in this course. Here are your learning materials:\n\n"

                        for material in course_details['materials']:
                           response += f"📚 {material['name']}\n"
                           response += f"   {material['url']}\n\n"

                        response += "Type 'show my courses' anytime to see your enrolled courses!"
                    else:
                         response = "I'm having trouble setting up your course. Please try again."

                else:
                    response = "I'm unable to find any content for the requested course. Please try again later."

            except Exception as e:
                logging.error(f"Error in course creation: {e}")  # Debug print
                response = "I encountered an error while setting up your course. Please try again."
        else:
            response = "Please provide both your experience level and coding interest. For example: 'I'm a beginner interested in data science'."

        dispatcher.utter_message(text=response)
        return [SlotSet("experience_level", experience), SlotSet("coding_interest", interest)]
class ActionShowEnrollments(Action):
    # Displays user's enrolled courses and their progress
    def __init__(self):
        super().__init__()
        self.lms = LMSManager()

    def name(self) -> Text:
        return "action_show_enrollments"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            user_id = tracker.sender_id
            logging.debug(f"Checking enrollments for user: {user_id}")  # Debug print

            courses = self.lms.get_user_courses(user_id)
            logging.debug(f"Retrieved courses: {courses}")  # Debug print

            if courses:
                response = "Here are your enrolled courses:\n\n"
                for course in courses:
                    response += f"📚 {course['name']}\n"
                    response += f"Status: {course['status']}\n"
                    response += f"Enrolled: {course['enrolled_at'][:10]}\n"
                    response += f"Completed Modules: {', '.join(course['completed_modules']) if course['completed_modules'] else 'None'}\n"
                    response += f"Completed Assessments: {', '.join(course['completed_assessments']) if course['completed_assessments'] else 'None'}\n\n"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text="You're not enrolled in any courses yet. Would you like some recommendations?")


        except Exception as e:
            logging.error(f"Error in ActionShowEnrollments: {e}")  # Debug print
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving your courses.")

        return []

class ActionDefaultWelcome(Action):
    def name(self) -> Text:
        return "action_default_welcome"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        lms = LMSManager()
        courses = [course.get("courseTitle") for course in lms._data.get("courses", [])]
        course_list = ", ".join(courses)
        dispatcher.utter_message(text=f"Hello! How can I help you today? I can provide information about following courses: {course_list}")
        return []
class ActionListCourses(Action):
    def name(self) -> Text:
        return "action_list_courses"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        lms = LMSManager()
        courses = [course.get("courseTitle") for course in lms._data.get("courses", [])]
        course_list = ", ".join(courses)
        dispatcher.utter_message(text=f"I can provide information about the following courses: {course_list}")
        return []

class ActionStartLearning(Action):
   def name(self) -> Text:
      return "action_start_learning"

   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      topic = tracker.get_slot("topic")
      user_id = tracker.sender_id
      lms = LMSManager()
      if topic:
          enrolled = lms.enroll_user(user_id, topic)
          if enrolled:
              dispatcher.utter_message(text=f"Okay, let's begin your learning journey on {topic}.")
              return [SlotSet("current_topic",topic)]
          else:
              dispatcher.utter_message(text="Sorry, I'm unable to enroll you in this course")
              return []
      else:
          dispatcher.utter_message(text="Please specify the topic you'd like to start learning about.")
          return []


class ActionGetTopicInfo(Action):
    def name(self) -> Text:
        return "action_get_topic_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
      topic = tracker.get_slot("topic")
      logging.debug(f"ActionGetTopicInfo: topic={topic}")
      if topic:
          try:
                lms = LMSManager()
                # Map short name to full course name
                if topic == "web":
                   full_topic_name = "Web Development"
                elif topic == "app":
                    full_topic_name = "App Development"
                elif topic == "python":
                   full_topic_name = "Python"
                elif topic == "java":
                   full_topic_name = "Java"
                elif topic == "c++":
                   full_topic_name = "C++"
                elif topic == "fullstack":
                   full_topic_name = "Full Stack Development"
                elif topic == "flutter":
                    full_topic_name = "Flutter"
                else:
                    full_topic_name = topic

                course_details = lms.get_course_details(full_topic_name)

                if course_details:
                    syllabus_str = ""
                    if "syllabus" in course_details and course_details["syllabus"]:
                      syllabus_str += "\nSyllabus:\n"
                      for module in course_details["syllabus"]:
                          syllabus_str += f"  - {module['moduleTitle']}\n"
                          for subtopic in module.get('subtopics', []):
                            syllabus_str += f"   -- {subtopic}\n"
                    else:
                       syllabus_str = "\nSyllabus not available."

                    resources_str = ""
                    if "materials" in course_details and course_details["materials"]:
                        resources_str += "\nResources:\n"
                        for material in course_details["materials"]:
                           resources_str += f" - {material['name']} : {material['url']}\n"

                    else:
                         resources_str = "\nNo resources available for this course."

                    learning_path_str = ""
                    if "syllabus" in course_details and course_details["syllabus"]:
                        learning_path_str += "\nLearning Path:\n"
                        learning_path_set = set()
                        for module in course_details['syllabus']:
                            learning_path_set.add(module['moduleTitle'])
                            for subtopic in module.get("subtopics", []):
                                learning_path_set.add(subtopic)
                        learning_path_str += "\n".join(f" {i+1}. {item}" for i,item in enumerate(learning_path_set))
                    else:
                       learning_path_str = "\nLearning path not available."
                    full_message = (
                        f"🎉 Welcome to {course_details['name']}!\n"
                        f"Description: {course_details['description']}\n"
                        f"{syllabus_str}"
                         f"{resources_str}"
                         f"{learning_path_str}"
                     )
                    dispatcher.utter_message(text=full_message)
                    return [SlotSet("topic", topic), SlotSet("course_details", course_details)]
                else:
                    dispatcher.utter_message(text=f"Sorry, I couldn't find any information on the course: {topic}.")
                    return [SlotSet("topic", topic), SlotSet("course_details", None)]

          except Exception as e:
              dispatcher.utter_message(text=f"Unable to fetch information about {topic}. Please try again later.")
              print("Error:", e)
              return [SlotSet("topic", topic), SlotSet("course_details", None)]
      else:
        dispatcher.utter_message(text="Please specify a topic to get information.")
      return []
class ActionGreet(Action):
     def name(self) -> Text:
         return "action_greet"
     def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        lms = LMSManager()
        courses = [course.get("courseTitle") for course in lms._data.get("courses", [])]
        course_list = ", ".join(courses)
        dispatcher.utter_message(text=f"Hello! 👋 Welcome to your personalized learning assistant. I can provide information about following courses: {course_list}")
        return []
class ActionEnrollInCourse(Action):
   def __init__(self):
       super().__init__()
       self.lms = LMSManager()
   def name(self) -> Text:
        return "action_enroll_in_course"

   def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      user_id = tracker.get_slot("user_id")
      topic = tracker.get_slot("topic")
      logging.debug(f"ActionEnrollInCourse: user_id={user_id}, topic={topic}")
      if topic:
            # Map short name to full course name
            if topic == "web":
                full_topic_name = "Web Development"
            elif topic == "app":
                full_topic_name = "App Development"
            elif topic == "python":
                full_topic_name = "Python"
            elif topic == "java":
                full_topic_name = "Java"
            elif topic == "c++":
                full_topic_name = "C++"
            elif topic == "fullstack":
                full_topic_name = "Full Stack Development"
            elif topic == "flutter":
                 full_topic_name = "Flutter"
            else:
                full_topic_name = topic
            enrolled = self.lms.enroll_user(user_id, full_topic_name)
            if enrolled:
                dispatcher.utter_message(text=f"Okay, you've been enrolled in {full_topic_name}.")
                return [SlotSet("current_topic", full_topic_name)]
            else:
                 dispatcher.utter_message(text="Sorry, I'm unable to enroll you in this course.")
                 return []
      else:
          dispatcher.utter_message(text="Please specify the course you'd like to enroll in.")
          return []
class ActionShowEnrolledCourses(Action):
   def __init__(self):
      super().__init__()
      self.lms = LMSManager()

   def name(self) -> Text:
      return "action_show_enrolled_courses"

   def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         user_id = tracker.sender_id
         logging.debug(f"Checking enrollments for user: {user_id}")
         courses = self.lms.get_user_courses(user_id)
         logging.debug(f"Retrieved courses: {courses}")

         if courses:
            response = "Here are your enrolled courses:\n\n"
            for course in courses:
                response += f"📚 {course['name']}\n"
                response += f"Status: {course['status']}\n"
                response += f"Enrolled: {course['enrolled_at'][:10]}\n"
                response += f"Completed Modules: {', '.join(course['completed_modules']) if course['completed_modules'] else 'None'}\n"
                response += f"Completed Assessments: {', '.join(course['completed_assessments']) if course['completed_assessments'] else 'None'}\n\n"

            dispatcher.utter_message(text=response)
         else:
             dispatcher.utter_message(text="You're not enrolled in any courses yet. Would you like some recommendations?")
         return []
class ActionStartQuiz(Action):
    def __init__(self):
       super().__init__()
       self.lms = LMSManager()

    def name(self) -> Text:
       return "action_start_quiz"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       topic = tracker.get_slot("topic")
       user_id = tracker.sender_id
       logging.debug(f"ActionStartQuiz: user_id={user_id}, topic={topic}")
       if topic:
            # Map short name to full course name
            if topic == "web":
               full_topic_name = "Web Development"
            elif topic == "app":
               full_topic_name = "App Development"
            elif topic == "python":
               full_topic_name = "Python"
            elif topic == "java":
               full_topic_name = "Java"
            elif topic == "c++":
               full_topic_name = "C++"
            elif topic == "fullstack":
               full_topic_name = "Full Stack Development"
            elif topic == "flutter":
               full_topic_name = "Flutter"
            else:
               full_topic_name = topic
            course_details = self.lms.get_course_details(full_topic_name)
            if course_details and 'quiz' in course_details:
                quiz = course_details['quiz']
                dispatcher.utter_message(text=f"Ok, here's the quiz for {full_topic_name}, please answer the question", buttons=[
                    {"title":option, "payload":f"answer_quiz{{'topic':'{topic}','answer':'{option}'}}"} for option in quiz['options']
                ])
                return[SlotSet("quiz_started",True)]
            else:
                 dispatcher.utter_message(text="Sorry, there is no quiz for the selected topic")
                 return []
       else:
            dispatcher.utter_message(text="Please specify the course for which you'd like to start a quiz.")
            return []

class ActionAnswerQuiz(Action):
   def __init__(self):
       super().__init__()
       self.lms = LMSManager()
   def name(self) -> Text:
       return "action_answer_quiz"

   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       user_id = tracker.sender_id
       intent_data = tracker.latest_message.get("intent", {}).get("name")
       logging.debug(f"ActionAnswerQuiz: user_id={user_id}, intent_data={intent_data}")
       answer = None
       topic = None
       if intent_data == "answer_quiz":
            data_str = tracker.latest_message["text"].split("answer_quiz", 1)[1].strip()
            data = json.loads(data_str)
            answer = data.get('answer')
            topic = data.get('topic')
            # Map short name to full course name
            if topic == "web":
                full_topic_name = "Web Development"
            elif topic == "app":
                full_topic_name = "App Development"
            elif topic == "python":
                full_topic_name = "Python"
            elif topic == "java":
                 full_topic_name = "Java"
            elif topic == "c++":
                full_topic_name = "C++"
            elif topic == "fullstack":
                full_topic_name = "Full Stack Development"
            elif topic == "flutter":
                full_topic_name = "Flutter"
            else:
               full_topic_name = topic
            course_details = self.lms.get_course_details(full_topic_name)
            if course_details and 'quiz' in course_details:
                correct_answer = course_details['quiz']['correct_answer']
                if answer == correct_answer:
                    self.lms.mark_assessment_completed(user_id,full_topic_name,course_details['quiz']['question'])
                    dispatcher.utter_message(text="Correct Answer! 🎉")
                    dispatcher.utter_message(text=f"Your quiz score is updated.")
                else:
                    dispatcher.utter_message(text=f"Wrong Answer! 😟. The correct answer is {correct_answer}")
                    dispatcher.utter_message(text=f"Your quiz score is updated.")
            return [SlotSet("topic",topic)]
       return []

class ActionMarkModuleComplete(Action):
  def __init__(self):
    super().__init__()
    self.lms = LMSManager()

  def name(self) -> Text:
    return "action_mark_module_complete"

  def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    user_id = tracker.sender_id
    topic = tracker.get_slot("topic")
    module = tracker.get_slot("module")
    logging.debug(f"ActionMarkModuleComplete: user_id={user_id}, topic={topic}, module={module}")
    if topic and module:
      # Map short name to full course name
      if topic == "web":
          full_topic_name = "Web Development"
      elif topic == "app":
        full_topic_name = "App Development"
      elif topic == "python":
          full_topic_name = "Python"
      elif topic == "java":
          full_topic_name = "Java"
      elif topic == "c++":
          full_topic_name = "C++"
      elif topic == "fullstack":
          full_topic_name = "Full Stack Development"
      elif topic == "flutter":
          full_topic_name = "Flutter"
      else:
        full_topic_name = topic
      self.lms.mark_module_completed(user_id, full_topic_name, module)
      dispatcher.utter_message(text=f"Okay, I've marked the {module} module as completed for the {full_topic_name} course.")
      return []
    else:
      dispatcher.utter_message(text="Please provide both the course and module name")
      return []
