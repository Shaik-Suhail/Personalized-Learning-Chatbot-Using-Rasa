# Personalized Learning Chatbot Using Rasa

This repository contains the code for a personalized learning chatbot designed to guide users through various programming courses. The chatbot leverages Rasa for conversational AI and Streamlit for the interactive user interface.

## Overview

The chatbot provides information about different programming courses, allows users to simulate enrollment, track their progress, and even take simple quizzes.

**Key Features:**

*   **Course Discovery:** Users can ask about specific topics (e.g., "web development", "Python") to view relevant courses and materials.
*   **Free Access Links:** It provides free access links to external resources where users can learn about their specific area of interest.
*   **Simulated Enrollment:** Users can simulate enrolling in a course, which makes a note of it and can be displayed in a list.
*   **Module Completion:** It allows for simulated module completion tracking with visual feedback, which helps users visualize the learning path.
*  **Simple Quizzes:** Users can test their knowledge with basic multiple choice quizzes after they are enrolled in a course.
*   **Interactive UI:** The application is using Streamlit for a user-friendly chat interface with an animated floating window for the "About" section.
*   **Rasa Powered:** The chatbot conversation logic is powered by Rasa, an open-source conversational AI framework.

## Technologies Used

*   **Python:** Primary language for the application and chatbot logic.
*   **Streamlit:** For the interactive user interface.
*   **Rasa:** For conversational AI and chatbot handling.
*   **Git:** For version control and code management.
* **Google Workspace** For the logo for the project.
*   **JSON:** For handling data files.
* **Vecteezy:** Used for the background image for the application

## Project Structure
Use code with caution.
Markdown
your_project_directory/
├── actions.py # Custom Rasa action code
├── app.py # Streamlit application code
├── style.css # Custom CSS style definitions
├── static/
| └── styles.css # Custom CSS style definitions
├── utils/
| └── lms_utils.py # Manages the JSON file for persistence
├── data/ # Rasa training data
│ └── nlu.yml # Training data for NLU
│ └── stories.yml # Defines conversation flows
│ └── rules.yml # Rules file for bot behavior
└── domain.yml # Rasa domain file

## Setup

1.  **Install Git:** If you haven't already, install Git on your local machine using these instructions: [https://git-scm.com/downloads](https://git-scm.com/downloads)
2.  **Clone the Repository:** Clone the repository to your local machine using the command:

    ```bash
    git clone [YOUR_GITHUB_REPOSITORY_URL]
    ```

    *(Replace `[YOUR_GITHUB_REPOSITORY_URL]` with the URL of your repository.)*
3.  **Navigate to the Project Folder:** Go to your project directory:
    ```bash
    cd your_project_directory
    ```
4.  **Install Dependencies:** Install the necessary Python packages using pip:

    ```bash
    pip install streamlit requests rasa rasa-sdk
    ```

5. **Train your Rasa model**:
    Run the following command to train the rasa model, and it should pick up all the changes made.
   ```bash
   rasa train
Use code with caution.
Running the Application

Start the Rasa Action Server: Open a new terminal and navigate to your project directory. Start the Rasa action server with:

rasa run actions
Use code with caution.
Bash
Start the Rasa server: Open another terminal window, and start the Rasa server with:

rasa run
Use code with caution.
Bash
Start the Streamlit App: Open a new terminal and navigate to your project directory, then start the Streamlit app with:

streamlit run app.py
Use code with caution.
Bash
This will launch the application in your default web browser.

Using the Chatbot

Initial Greeting: The bot will display the welcome message with all available courses.

Course Discovery: Use the chat input to ask about a specific topic. E.g. "tell me about web development", "start learning python", etc.

Enrollment: Click the Enroll button to simulate enrollment in the course.

Module Completion: You can click on the module buttons to see the information about each module, and mark modules as complete by clicking the "Mark as Complete" button.

View Enrolled Courses: Type "show my courses" to see a list of your enrolled courses and their current status, as well as the list of completed modules for each course.

Start Quizzes: Click on "Start Quiz" button to start the quiz for the enrolled course.

About Window: Click on the "About Learning Assistant" button to view the information about the chat bot in the floating window.

Provide Feedback: Feel free to use keywords like "thanks", "great", "good", etc. to give feedback to the bot.

Future Improvements (Optional)

Persistent User Data: Implement a database or API for saving user progress and data across sessions.

User Authentication: Add a login system so each user can have their own progress tracking.

External APIs: Integrate with learning platforms APIs (like Coursera, Udemy) for real-time progress tracking.

Improved Quizzes: Make the quizzes more comprehensive and include different types of questions.

More Courses: Increase the list of courses and add more details to them, including detailed syllabus, module content and learning objectives.

Dynamic Content: Fetch the courses from external resources so that the content is dynamic and you do not need to redeploy every time you need to add a course.

Credits

This project uses the following open-source libraries: Streamlit, Rasa.

The background image used in this application was downloaded from Vecteezy

License

This project is under MIT License

Contribute

If you want to contribute to this project, you can open a pull request and I will review and merge it after reviewing the codes.
