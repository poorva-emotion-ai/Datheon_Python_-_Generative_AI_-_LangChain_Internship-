
import os
from dotenv import load_dotenv
from smolagents import OpenAIServerModel, CodeAgent

from tools import (
    create_revision_plan,
    evaluate_answer,
    web_search,
    calculator,
    read_local_file,
)

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from your .env file.")

gemini_model = OpenAIServerModel(
    model_id="gemini-3.5-flash",
    api_key=GEMINI_API_KEY,
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
)

student_agent = CodeAgent(
    tools=[
        create_revision_plan,
        evaluate_answer,
        web_search,
        calculator,
        read_local_file,
    ],
    model=gemini_model,
    max_steps=6,
)
