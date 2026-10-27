# StudyPilot-AI — AI Student Revision Agent

StudyPilot-AI is an AI-powered study assistant built with Python and Streamlit. It helps students revise topics, summarize notes, generate quizzes, and create personalized revision plans.

## Features

- **Ask AI Agent:** Ask questions and receive AI-generated responses.
- **Summarize Notes:** Generate concise summaries of study material.
- **Revision Planner:** Create a day-wise revision plan for selected topics.
- **Generate Quiz:** Generate quiz questions for practice.

## Technologies Used

- Python
- Streamlit
- smolagents
- OpenAI-compatible model interface
- Python tools and environment variables

## Project Structure

```text
StudyPilot-AI/
├── app.py
├── agent.py
├── tools.py
├── test.py
├── test_agent.py
├── robot.jpg
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment.
4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file and configure the API credentials required by the project. Never upload your API key to GitHub.
6. Start the application:

   ```bash
   streamlit run app.py
   ```

7. Open the local URL displayed in the terminal.

## Running Tests

Run the available test scripts from the project folder:

```bash
python test.py
python test_agent.py
```

## Security

API credentials and local environment files must remain private. The `.env` file and virtual environment are excluded through `.gitignore`.

## Project Status

The application and its main features have been tested locally. This repository contains the source code and setup instructions for review.
