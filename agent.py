import os
from dotenv import load_dotenv
from smolagents import OpenAIServerModel, CodeAgent 

from tools import(create_revision_plan,
        evaluate_answer
        )

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_model = OpenAIServerModel(
    model_id="gemini-3.5-flash",
    api_key=GEMINI_API_KEY,
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/"
)

student_agent = CodeAgent(
    tools=[
        create_revision_plan,
        evaluate_answer
    ],
    model=gemini_model
)