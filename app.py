import streamlit as st
import requests
import json
from datetime import datetime
import random
from typing import Any, Text, Dict, List
import os


# Load CSS from an external file
def load_css(file_path):
    with open(file_path, "r") as f:
      css = f"<style>{f.read()}</style>"
      st.markdown(css, unsafe_allow_html=True)

# Apply the CSS
load_css(os.path.join("static", "styles.css"))


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "enrolled_courses" not in st.session_state:
    st.session_state.enrolled_courses = []
if "user_progress" not in st.session_state:
    st.session_state.user_progress = {} # Initialize user progress
if "about_window_visible" not in st.session_state:
     st.session_state.about_window_visible = False # Initialize the visibility

# Define materials for all topics with free access links
COURSE_MATERIALS = {
    "web": {
        "name": "Web Development for Beginners",
        "materials": [
            {
                "name": "freeCodeCamp Web Development",
                "url": "https://www.freecodecamp.org/learn/responsive-web-design/",
                  "youtube_url": "https://www.youtube.com/watch?v=mU6anWqZJcc"
            },
            {
                "name": "MDN Web Docs",
                "url": "https://developer.mozilla.org/en-US/docs/Learn",
                  "youtube_url": "https://www.youtube.com/watch?v=3Jb-S0_u11Q"
            },
            {
                "name": "The Odin Project",
                "url": "https://www.theodinproject.com/",
                "youtube_url": "https://www.youtube.com/watch?v=na-x-Q13Kk4"
            }
        ],
        "description": "A curated learning path for beginners in web development. Free access to resources provided.",
        "modules": [
            {
                "title": "HTML Basics",
                "description": "Learn the fundamental building blocks of web pages.",
                "content": "Start with tags, elements and attributes"
            },
            {
                "title": "CSS Fundamentals",
                "description": "Style your HTML with CSS selectors and properties.",
                  "content": "Learn CSS selectors, and styling"
            },
             {
                "title": "JavaScript Introduction",
                "description":"Introduction to JavaScript. Learn about variable declaration, control flow, loops, and data types.",
                "content":"Learn how to use variables, loops, and datatypes in JS"
            },
            {
               "title": "JavaScript Frameworks",
                "description": "Learn about modern JS Frameworks",
                  "content": "Explore Javascript frameworks like React, Angular and Vue"
            }

        ],
          "quiz":{
            "question": "Which is not a javascript framework?",
            "options":["React", "Vue", "Java","Angular"],
             "correct_answer":"Java"
          }
    },
    "app": {
        "name": "App Development for Beginners",
        "materials": [
            {
                "name": "Android Developer Fundamentals",
                "url": "https://developer.android.com/courses",
                  "youtube_url":"https://www.youtube.com/watch?v=fis26AB2y0M"
            },
            {
                "name": "iOS App Development with Swift",
                "url": "https://developer.apple.com/tutorials/swiftui",
                  "youtube_url": "https://www.youtube.com/watch?v=ZJ08-j0Kz7s"
            },
              {
                "name": "React Native Tutorial",
                "url": "https://reactnative.dev/docs/tutorial",
                  "youtube_url": "https://www.youtube.com/watch?v=qZ3yZls8FzQ"
            }

        ],
        "description": "Learn to build mobile apps for iOS and Android. Free access to resources provided.",
        "modules": [
          {
              "title": "Platform Selection",
              "description": "Decide between Android and iOS development.",
              "content": "Choose the platform you want to learn, and select an IDE"
            },
            {
                "title": "Android basics",
                "description": "Learn basics of android development.",
                "content": "Start building your first android app"
            },
             {
                "title": "IOS basics",
                 "description": "Learn basics of IOS development",
                "content": "Start building your first IOS app"
            },
              {
                 "title": "React Native Basics",
                "description": "Learn basics of React Native Development",
                  "content":"Learn components and props of react native"
            }
         ],
          "quiz":{
            "question": "Which one is the cross platform mobile framework?",
             "options":["Swift", "Kotlin", "React Native","Java"],
             "correct_answer":"React Native"
          }
    },
    "python": {
        "name": "Python Programming for Beginners",
        "materials": [
             {
                "name": "Google's Python Class",
                "url": "https://developers.google.com/edu/python/",
                  "youtube_url": "https://www.youtube.com/watch?v=nwjAH-e_xmo"
            },
            {
                "name": "Learn Python.org",
                 "url": "https://www.learnpython.org/",
                  "youtube_url":"https://www.youtube.com/watch?v=rfscVS0vtbw"
            },
             {
                "name": "Python Crash Course",
                "url": "https://ehmatthes.github.io/pcc_2e/index.html",
                "youtube_url":"https://www.youtube.com/watch?v=JJmcL1N2KQs"
            }
        ],
         "description": "A comprehensive introduction to Python. Free access to resources provided.",
         "modules": [
             {
                 "title":"Introduction to Python",
                 "description": "Learn the fundamentals of Python programming language",
                   "content":"Start with variables, operators, and comments in python"
             },
             {
               "title": "Data structures in Python",
               "description": "Learn different datatypes in Python",
               "content":"Learn about lists, tuples, and dictionaries"
             },
             {
               "title": "Control Structures in Python",
               "description": "Learn about if/else and loops",
               "content":"Learn how to use if/else and for/while loops"
             },
             {
               "title": "Writing functions in python",
                 "description": "Learn how to write functions",
                  "content":"Start writing simple functions in python"
             }
         ],
          "quiz":{
            "question": "Which is the correct way to define a list in python?",
            "options":["(1,2,3)","[1,2,3]","{1,2,3}","list(1,2,3)"],
              "correct_answer":"[1,2,3]"
          }
     },
       "java": {
        "name": "Java Programming for Beginners",
        "materials": [
             {
                "name": "Java Programming Masterclass for Software Developers",
                "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
                   "youtube_url": "https://www.youtube.com/watch?v=eIrMbAQSU34"
             },
             {
                 "name": "Java Tutorial for Complete Beginners",
                 "url": "https://www.udemy.com/course/java-tutorial/",
                 "youtube_url": "https://www.youtube.com/watch?v=grEKqfRk_Gg"
             },
              {
                 "name": "Core Java Tutorial",
                 "url": "https://www.javatpoint.com/core-java-tutorial",
                   "youtube_url":"https://www.youtube.com/watch?v=xk4_1vDrzzo"
             }
        ],
        "description": "A comprehensive introduction to Java. Free access to resources provided.",
        "modules": [
            {
                "title": "Java Basics",
                "description": "Learn the fundamental of Java",
                "content":"Start by writing your first java program"
             },
              {
                 "title":"Data Structures",
                 "description": "Learn about different datatypes",
                 "content": "Learn int, string, boolean, and other types"
            },
              {
                "title":"Control structures in Java",
                "description":"Learn about loops and control structures",
                 "content": "Explore if/else, and for and while loops"
              },
              {
                 "title":"Functions in java",
                  "description":"Learn about functions",
                  "content": "Explore how to write functions in Java"
             }
        ],
          "quiz":{
            "question": "Which is not a primitive datatype in Java?",
            "options":["int","String","boolean","float"],
              "correct_answer":"String"
          }
    },
      "c++": {
          "name": "C++ Programming for Beginners",
        "materials": [
            {
                "name": "Learn CPP",
                "url": "https://www.learncpp.com/",
                   "youtube_url":"https://www.youtube.com/watch?v=rub_m5t30_s"
            },
            {
                "name": "C++ Tutorial",
                "url": "https://www.w3schools.com/cpp/default.asp",
                  "youtube_url":"https://www.youtube.com/watch?v=0jD7a51_bA4"
            },
              {
                 "name": "C++ Tutorial for Beginners",
                 "url": "https://www.udemy.com/course/free-learn-cpp-tutorial-beginners/",
                  "youtube_url":"https://www.youtube.com/watch?v=Mv0m407f7bM"
             }
        ],
          "description": "A comprehensive introduction to C++. Free access to resources provided.",
           "modules":[
                 {
                     "title": "C++ Fundamentals",
                     "description":"Learn about basics of C++",
                     "content":"Start with your first C++ program"
                 },
                  {
                      "title": "C++ Datatypes",
                      "description":"Learn about datatypes",
                      "content":"Learn different datatypes like int, char, float"
                  },
                   {
                      "title":"C++ Control Structures",
                      "description":"Learn about control flow",
                      "content":"Explore if/else, and for/while loops"
                   },
                   {
                       "title":"Functions in C++",
                       "description":"Learn about functions in C++",
                       "content":"Learn how to write functions in C++"
                   }
              ],
               "quiz":{
                "question": "Which of the following is not a valid operator in C++?",
                 "options":["+","--","<>","*"],
                  "correct_answer":"<>"
              }
          },
         "fullstack": {
            "name": "Full Stack Development for Beginners",
             "materials": [
                {
                  "name": "The Full Stack Open",
                    "url": "https://fullstackopen.com/en/",
                      "youtube_url":"https://www.youtube.com/watch?v=h2V-v75p0-k"
                },
                 {
                  "name": "Full Stack Web Development with React",
                    "url": "https://www.udemy.com/course/full-stack-react-with-hooks-nodejs-express-mongodb/",
                       "youtube_url": "https://www.youtube.com/watch?v=pU9abp7g8zU"
                },
                 {
                     "name": "freeCodeCamp Backend Development and APIs",
                     "url": "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
                      "youtube_url": "https://www.youtube.com/watch?v=G10E2_w9q_U"
                }
            ],
             "description": "A comprehensive introduction to Full Stack. Free access to resources provided.",
              "modules":[
                {
                     "title":"Frontend Basics",
                    "description": "Learn the front-end technologies",
                      "content":"Start with HTML, CSS and Javascript"
                 },
                {
                   "title":"Backend Fundamentals",
                   "description": "Learn the backend technologies",
                   "content": "Start with Node.js, and express"
                 },
                {
                    "title":"Connecting Frontend and Backend",
                    "description": "Learn the architecture of full stack app",
                    "content":"Learn about the flow of data"
                },
                 {
                    "title":"Database and Deployment",
                    "description": "Learn about databases and deploying your fullstack application",
                      "content": "Learn databases and deploying your app"
                }
              ],
              "quiz":{
                "question": "What is the purpose of a REST API?",
                 "options":["To style webpage","To perform database query", "To enable communication between web services","To manage network traffic"],
                 "correct_answer":"To enable communication between web services"
              }
        },
       "flutter": {
            "name": "Flutter Development for Beginners",
            "materials": [
                 {
                    "name":"Flutter Documentation",
                    "url": "https://docs.flutter.dev/",
                     "youtube_url":"https://www.youtube.com/watch?v=VPvVD8t02jU"
                },
                {
                     "name": "Flutter Course by Angela Yu",
                     "url": "https://www.udemy.com/course/flutter-bootcamp-with-dart/",
                        "youtube_url":"https://www.youtube.com/watch?v=pTJgUo2gG8k"
                },
                {
                   "name": "Flutter Tutorial",
                   "url": "https://www.youtube.com/watch?v=x0uinJvhlnI",
                   "youtube_url": "https://www.youtube.com/watch?v=x0uinJvhlnI"
               }
    
        ],
         "description": "A comprehensive introduction to Flutter. Free access to resources provided.",
        "modules": [
            {
                "title":"Introduction to Flutter",
                "description":"Learn about flutter fundamentals",
                 "content":"Start by setting up your flutter environment"
            },
             {
                 "title":"Flutter UI Fundamentals",
                "description":"Learn basics of flutter UI",
                "content": "Learn about different widgets"
             },
             {
                 "title":"Widget Tree",
                 "description": "Learn about how flutter widgets are rendered",
                  "content":"Understand the widget tree"
              },
               {
                   "title": "Cross Platform Functionality",
                   "description": "Learn how to build cross platform apps",
                    "content":"Build simple flutter apps"
                }
         ],
          "quiz":{
            "question": "What language is primarily used in Flutter?",
            "options":["Swift","Kotlin","Dart","Java"],
             "correct_answer":"Dart"
          }
    },
}
# Rasa endpoint
RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

# Helper Functions
def send_message_to_rasa(message: str) -> List[Dict[str, Any]]:
     payload = {"sender": "user", "message": message}
     headers = {'Content-type': 'application/json'}
     try:
        response = requests.post(RASA_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
     except requests.exceptions.RequestException as e:
         st.error(f"Error connecting to Rasa: {e}")
         return []

def display_bot_response(response: List[Dict[str, Any]]) -> None:
    for message in response:
        if "text" in message:
            with st.container():
               st.markdown(f"""
                     <div class="message-container">
                            <div class="bot-avatar message-avatar"></div>
                            <div class="bot-message">
                              <p>{message["text"]}</p>
                             </div>
                     </div>

                """, unsafe_allow_html=True)
        if "buttons" in message:
            with st.chat_message("assistant"):
                 for button in message['buttons']:
                      if st.button(button['title'],key=random.random()):
                         response = send_message_to_rasa(button['payload'])
                         display_bot_response(response)

def display_bot_message(message: str) -> None:
   with st.container():
       st.markdown(f"""
           <div class="message-container">
               <div class="bot-avatar message-avatar"></div>
                <div class="bot-message">
                   <p>{message}</p>
                </div>
           </div>
       """, unsafe_allow_html=True)

# Function to handle initial greeting
def handle_initial_greeting() -> None:
    if not st.session_state.messages:
       response = send_message_to_rasa("default_welcome")
       if response:
          st.session_state.messages.append({"role": "assistant", "content": response[0].get("text","")})
          display_bot_message(response[0].get("text",""))

def get_feedback_response(prompt: str) -> str | None:
    import random
    FEEDBACK_RESPONSES = {
        "thanks": [
            "You're welcome! 😊 Let me know if you need anything else!",
            "Happy to help! 🌟 Feel free to explore more courses!",
            "Glad I could help! 🎉 Don't forget you can check your courses anytime!"
        ],
        "good": [
            "Thank you for the feedback! 🌟 Is there anything else you'd like to learn?",
            "Wonderful! 🎉 Let me know if you want to explore more topics!",
            "Great to hear that! 😊 Feel free to ask about other courses!"
        ],
        "bye": [
            "Goodbye! 👋 Come back anytime to continue learning!",
            "See you later! 🌟 Your courses will be here when you return!",
            "Have a great day! 😊 Don't forget to practice what you've learned!"
        ],
        "hello": [
            "Hi there! 👋 Ready to learn something new?",
            "Hello! 🌟 What would you like to learn today?",
            "Welcome! 😊 I can help you find the perfect course!"
        ]
    }
    if any(word in prompt for word in ["thanks", "thank you", "thx"]):
        return random.choice(FEEDBACK_RESPONSES["thanks"])
    elif any(word in prompt for word in ["good", "great", "awesome", "amazing"]):
        return random.choice(FEEDBACK_RESPONSES["good"])
    elif any(word in prompt for word in ["bye", "goodbye", "see you"]):
        return random.choice(FEEDBACK_RESPONSES["bye"])
    elif any(word in prompt for word in ["hi", "hello", "hey"]):
        return random.choice(FEEDBACK_RESPONSES["hello"])
    return None

def get_course_materials(topic: str) -> dict | None:

    if topic in COURSE_MATERIALS:
      course =  COURSE_MATERIALS[topic]
      return course
    else:
      return None


def check_input_requirements(prompt: str) -> str | None:
    has_experience = any(word in prompt for word in ["beginner", "intermediate", "advanced"])
    has_topic = any(word in prompt for word in ["web", "app", "python", "java", "cpp", "fullstack", "flutter"])

    if not has_experience and not has_topic:
        return "Please provide both your experience level (beginner/intermediate/advanced) and interest area. For example: 'I'm a beginner interested in web development'"
    elif not has_experience:
        return "Please specify your experience level (beginner/intermediate/advanced). For example: 'I'm a beginner'"
    elif not has_topic:
        return "Please specify what you'd like to learn (web development, app development, Python, Java, C++, Full Stack or Flutter)"
    return None

def display_course_response(topic: str) -> tuple[str, List[Dict[str,str]]]:
    course = COURSE_MATERIALS[topic]
    response_text = f"🎉 Welcome to {course['name']}!"
    st.markdown(response_text)
    st.markdown('<div class="animated-tab">Personalized Learning Chatbot</div>', unsafe_allow_html=True)
    st.write("📚 **Learning Materials:**")
    for material in course['materials']:
        st.markdown(f"• [{material['name']}]({material['url']})")
        if 'youtube_url' in material:
          st.markdown(f"  🎬 [Watch tutorial]({material['youtube_url']})")
    st.write("\n📝 **Course Description:**")
    st.write(course['description'])
    st.info("💡 **Learning Path:**\n")

    # Display modules with completion buttons
    if 'modules' in course:
        for i, module in enumerate(course['modules']):
            module_key = f"{topic}_module_{i}"
            completed = False
            if topic in st.session_state.user_progress and 'completed_modules' in st.session_state.user_progress[topic]:
                if module['title'] in st.session_state.user_progress[topic]['completed_modules']:
                  completed= True
            with st.expander(f"{i+1}. {module['title']}"):
                st.write(f"**Description:** {module['description']}")
                if 'content' in module:
                  st.write(f"**Content:** {module['content']}")
                if completed:
                  st.success(f"Module completed")
                else:
                  if st.button(f"Mark {module['title']} as Complete", key=module_key):
                      if topic not in st.session_state.user_progress:
                          st.session_state.user_progress[topic]= {
                              "completed_modules": [module["title"]]
                         }
                      else:
                        if 'completed_modules' not in st.session_state.user_progress[topic]:
                              st.session_state.user_progress[topic]['completed_modules'] = [module["title"]]
                        elif module['title'] not in st.session_state.user_progress[topic]['completed_modules']:
                            st.session_state.user_progress[topic]['completed_modules'].append(module['title'])
                      st.success(f"Module {module['title']} marked as complete.")


    # Check if the user is already enrolled
    is_enrolled = topic in [enrolled_course['topic'] for enrolled_course in st.session_state.enrolled_courses]
    # Add a button to enroll
    if is_enrolled:
       st.button(f"Enrolled in {course['name']}", key = f"enroll_{topic}", disabled=True)
    else:
      if st.button(f"Enroll in {course['name']}", key = f"enroll_{topic}"):
          if topic not in [ enrolled_course['name'].lower() for enrolled_course in st.session_state.enrolled_courses]:
              course_entry = {
                  "name": course['name'],
                  "enrolled_at": datetime.now().strftime("%Y-%m-%d"),
                  "status": "In Progress",
                   "materials": course['materials'],
                  "topic":topic
              }
              st.session_state.enrolled_courses.append(course_entry)
              st.success(f"You are now enrolled in {course['name']}!")
              st.session_state.messages.append({
                        "role":"assistant",
                        "content": f"You are now enrolled in {course['name']}!"
                    })
          else:
             st.warning(f"You are already enrolled in {course['name']}!")
             st.session_state.messages.append({
                        "role":"assistant",
                        "content": f"You are already enrolled in {course['name']}!"
                    })
    return response_text, course['materials']


def show_enrolled_courses():
    if st.session_state.enrolled_courses:
        response_text = "Here are your enrolled courses:\n\n"
        for course in st.session_state.enrolled_courses:
            response_text += f"📚 {course['name']}\n"
            response_text += f"Status: {course['status']}\n"
            response_text += f"Enrolled: {course['enrolled_at']}\n"
            if course['topic'] in st.session_state.user_progress and 'completed_modules' in st.session_state.user_progress[course['topic']]:
               completed_modules = st.session_state.user_progress[course['topic']]['completed_modules']
               response_text += f"Completed Modules: {', '.join(completed_modules)}\n"
            else:
                response_text += f"Completed Modules: None\n"
            if  st.button(f"Start Quiz for {course['name']}", key=f"quiz_{course['name']}"):
                  start_quiz(course["topic"], course['name'])
        st.markdown(response_text)


    else:
        st.markdown("You're not enrolled in any courses yet. Would you like some recommendations?")

def start_quiz(topic:str, course_name:str):
      quiz = COURSE_MATERIALS[topic]['quiz']
      st.session_state.quiz_started= True
      if topic not in st.session_state.user_progress:
         st.session_state.user_progress[topic] = {
             "course_name": course_name,
              "completed_modules": [],
             "quiz_score":0,
             "question_asked": quiz['question'],
             "options":quiz['options'],
              "correct_answer":quiz['correct_answer']
         }
      else:
           st.session_state.user_progress[topic]['question_asked'] = quiz['question']
           st.session_state.user_progress[topic]['options'] = quiz['options']
           st.session_state.user_progress[topic]['correct_answer'] = quiz['correct_answer']

      st.session_state.messages.append({
              "role":"assistant",
              "content":f"Ok, here's the quiz for {course_name}, please answer the question"
           })

      with st.chat_message("assistant"):
           st.write(f"**{st.session_state.user_progress[topic]['question_asked']}**")
           user_answer = st.radio("Select answer", st.session_state.user_progress[topic]['options'], key=f"radio_{course_name}_{random.random()}")

           if user_answer:
                if user_answer == st.session_state.user_progress[topic]["correct_answer"]:
                     st.session_state.user_progress[topic]['quiz_score'] += 1
                     st.success("Correct Answer")
                     st.session_state.messages.append({
                       "role": "assistant",
                       "content": f"Your quiz score is {st.session_state.user_progress[topic]['quiz_score']}"
                     })
                else:
                    st.error("Wrong Answer")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Your quiz score is {st.session_state.user_progress[topic]['quiz_score']}"
                     })

# Rasa endpoint
RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

# Display chat messages from history
with st.container():
  st.markdown('<div class="chat-container"><div class="chat-messages" id="chat-messages"></div></div>', unsafe_allow_html=True)
  for message in st.session_state.messages:
      with st.container():
        if message["role"] == "user":
          st.markdown(f'<div class="message-container user-message-container"><div class="user-avatar message-avatar"></div><div class="user-message"><p>{message["content"]}</p></div></div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
           display_bot_message(message["content"])
           if "materials" in message:
               st.write("📚 **Learning Materials:**")
               for material in message["materials"]:
                    st.markdown(f"• [{material['name']}]({material['url']})")
                    if 'youtube_url' in material:
                       st.markdown(f"  🎬 [Watch tutorial]({material['youtube_url']})")

# Toggle for the floating window
if st.button("About Learning Assistant", key="about_button"):
   st.session_state.about_window_visible = not st.session_state.about_window_visible

# Display floating window conditionally
if st.session_state.about_window_visible:
   with st.container():
    st.markdown(f"""
          <div class="floating-window {'hidden' if not st.session_state.about_window_visible else ''}">
             <h2>About Learning Assistant</h2>
                <p>This chatbot helps you find the right programming courses based on your experience level and interests.</p>
               <p>Try asking about:</p>
                  <ul>
                   <li>Web Development</li>
                    <li>Data Science</li>
                    <li>Mobile Apps</li>
                     <li>Artificial Intelligence</li>
                   </ul>
           </div>
        """, unsafe_allow_html=True)

# Display the animated tab with the application name
st.markdown('<div class="animated-tab">Personalized Learning Chatbot</div>', unsafe_allow_html=True)

# Handle initial welcome
handle_initial_greeting()


# Accept user input
if prompt := st.chat_input("What would you like to learn?", key="chat_input"):
    prompt = prompt.lower()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
       st.markdown(f'<div class="message-container user-message-container"><div class="user-avatar message-avatar"></div><div class="user-message"><p>{prompt}</p></div></div>', unsafe_allow_html=True)


     # Send user message to rasa
    response = send_message_to_rasa(prompt)
    if response:
       # Add bot responses to the session state
       for message in response:
            if "text" in message:
                st.session_state.messages.append({"role": "assistant", "content": message["text"]})
            display_bot_response([message])
       # Check for topic matches
    topic = None
    if "web" in prompt or 'web development' in prompt :
        topic = "web"
    elif "app" in prompt or 'app development' in prompt:
         topic = "app"
    elif "python" in prompt:
        topic = "python"
    elif "java" in prompt:
         topic = "java"
    elif "c++" in prompt or "cpp" in prompt:
         topic = "c++"
    elif "fullstack" in prompt or "full stack" in prompt:
        topic = "fullstack"
    elif "flutter" in prompt:
        topic = "flutter"
    if topic:
        course_details = get_course_materials(topic)
        if course_details:
            with st.chat_message("assistant"):
                 response_text, materials = display_course_response(topic)
                 st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text,
                         "materials":materials
                     })
    elif "show my courses" in prompt:
        with st.chat_message("assistant"):
            show_enrolled_courses()
    # Check for requirements if user asked any other type of input
    if not any(word in prompt for word in ["show my courses", "show enrollments"]):
       requirement_message = check_input_requirements(prompt)
       if requirement_message:
          with st.chat_message("assistant"):
              st.markdown(f'<div class="bot-message"><p>{requirement_message}</p></div>', unsafe_allow_html=True)
    # Handle feedback after bot responses
    feedback_response = get_feedback_response(prompt)
    if feedback_response:
        with st.chat_message("assistant"):
              st.markdown(f'<div class="message-container"><div class="bot-avatar message-avatar"></div><div class="bot-message"><p>{feedback_response}</p></div></div>', unsafe_allow_html=True)