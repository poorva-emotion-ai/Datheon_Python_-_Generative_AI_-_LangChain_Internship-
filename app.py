import base64
import json
import re
import streamlit as st
from pathlib import Path
from agent import student_agent, gemini_model
from smolagents import ChatMessage
from tools import create_revision_plan, evaluate_answer



# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="StudyPilot-AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- MOCHA THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

:root {
    --mocha: #49352d;
    --mocha-light: #775849;
    --cream: #fcf7f1;
    --text: #34251f;
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: #fcf8f3;
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #49352d, #35251f);
    border-right: 1px solid #6a4d40;
}

[data-testid="stSidebar"] * {
    color: #fff4e9 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 10px 12px;
    border-radius: 12px;
    margin-bottom: 5px;
    font-size: 15px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #654a3d;
}

/* Headings */
h1, h2, h3 {
    color: #392820 !important;
    font-weight: 800 !important;
}

p, li {
    color: #6c5a50;
    font-size: 15px;
}

/* Welcome banner */
.hero {
    background: linear-gradient(115deg, #f7e8dc, #fff8ef 65%, #f0dfd1);
    border: 1px solid #ead7c8;
    border-radius: 25px;
    padding: 30px;
    min-height: 230px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    margin-bottom: 26px;
}

.hero h1 {
    font-size: clamp(30px, 3vw, 43px);
    margin: 0 0 8px 0;
}

.hero h3 {
    color: #916751 !important;
    font-size: 21px;
    margin: 0 0 14px 0;
}

.hero p {
    font-size: 16px;
    line-height: 1.7;
    margin-bottom: 0;
}

.hero img {
    width: 210px;
    max-width: 100%;
    object-fit: contain;
}

/* Feature cards */
.feature-card {
    border-radius: 21px;
    padding: 23px 21px;
    min-height: 225px;
    border: 1px solid #eaded6;
    margin-bottom: 10px;
}

.feature-card .emoji {
    font-size: 32px;
    margin-bottom: 12px;
}

.feature-card h3 {
    font-size: 19px;
    margin: 0 0 10px 0;
}

.feature-card p {
    line-height: 1.6;
    min-height: 48px;
    margin-bottom: 0;
}

.card-blue {
    background: linear-gradient(140deg, #edf0fa, #f5f4fa);
}

.card-green {
    background: linear-gradient(140deg, #edf4e9, #f8f6ec);
}

.card-purple {
    background: linear-gradient(140deg, #f1e9f5, #f8f0f7);
}

.card-peach {
    background: linear-gradient(140deg, #fbe9dd, #fff3e9);
}

/* Buttons */
.stButton > button {
    border-radius: 13px;
    border: 1px solid #d9b9a4;
    background: #775747;
    color: white;
    font-weight: 700;
    min-height: 43px;
    transition: 0.2s ease;
}


/* All tool buttons: readable text */
.stButton > button,
.stButton > button p {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: #775747 !important;
    border: 1px solid #775747 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* Hover */
.stButton > button:hover,
.stButton > button:hover p {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: #5a4033 !important;
    border-color: #5a4033 !important;
}

/* Disabled buttons: keep the label readable */
.stButton > button:disabled,
.stButton > button:disabled p {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
}

}


/* Typed text in input fields */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
[data-testid="stChatInput"] textarea {
    color: #34251f !important;
    -webkit-text-fill-color: #34251f !important;
    caret-color: #34251f !important;
    background-color: #fffdfb !important;
    opacity: 1 !important;
}

/* Placeholder text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: #8b776b !important;
    -webkit-text-fill-color: #8b776b !important;
    opacity: 1 !important;
}


/* Ask AI Agent: chat input */
[data-testid="stChatInput"] textarea {
    color: #34251f !important;
    -webkit-text-fill-color: #34251f !important;
    caret-color: #34251f !important;
    background-color: #fffdfb !important;
    opacity: 1 !important;
}

/* Chat input placeholder */
[data-testid="stChatInput"] textarea::placeholder {
    color: #8b776b !important;
    -webkit-text-fill-color: #8b776b !important;
    opacity: 1 !important;
}


[data-testid="stChatMessage"] {
    background: #fffaf5;
    border: 1px solid #eee0d5;
    border-radius: 16px;
}

/* Quick tips */
.tips {
    background: linear-gradient(110deg, #f7eae0, #fff8f0);
    border: 1px solid #ead8c9;
    border-radius: 22px;
    padding: 22px 25px;
    margin-top: 17px;
}

.tips h3 {
    margin-top: 0;
}

.small-note {
    color: #8b6d5c;
    font-size: 13px;
}

hr {
    border-color: #eadbd0;
}

@media (max-width: 700px) {
    .hero {
        padding: 20px;
    }
    .hero img {
        width: 100px;
    }
}

<CodeBlock language="css" editable>
/* Revision Planner: keep content within a comfortable width */
[data-testid="stTextArea"],
[data-testid="stNumberInput"] {
    max-width: 850px;
}


/* Improve input appearance */
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
color: #34251f !important;
background-color: #fffdfb !important;
border: 1px solid #d9c5b7 !important;
border-radius: 12px !important;
}

/* Revision Planner button */
.stButton > button {
color: #ffffff !important;
background-color: #775747 !important;
border: 1px solid #775747 !important;
opacity: 1 !important;
}

.stButton > button:disabled {
color: #ffffff !important;
background-color: #a38a7b !important;
opacity: 0.75 !important;
}
</CodeBlock>
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""


def get_response_text(response):
    """Extract readable text from smolagents ChatMessage/model responses."""
    content = getattr(response, "content", None)
    if isinstance(content, str):
        return content
    if content is not None:
        return str(content)
    return str(response)


# ---------------- NAVIGATION ----------------
pages = [
    "Home",
    "Ask AI Agent",
    "Summarize Notes",
    "Revision Planner",
    "Generate Quiz",
    "Settings",
]

page_icons = {
    "Home": "🏡",
    "Ask AI Agent": "💬",
    "Summarize Notes": "📖",
    "Revision Planner": "🗓️",
    "Generate Quiz": "✏️",
    "Settings": "⚙️",
}

# The callback updates the page and the radio widget together.
def navigate_to(page):
    st.session_state.page = page
    st.session_state.page_navigation = page


with st.sidebar:
    st.markdown("""
    <div style="padding:15px 5px 25px 5px;">
        <div style="font-size:35px;">📚</div>
        <div style="font-size:25px;font-weight:800;">StudyPilot-AI</div>
        <div style="font-size:14px;color:#ead1bd;">
            Your AI Study Companion
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Initialize the widget's state before creating the radio.
    if "page_navigation" not in st.session_state:
        st.session_state.page_navigation = st.session_state.page

    selected_page = st.radio(
        "Navigation",
        pages,
        format_func=lambda p: f"{page_icons[p]}   {p}",
        label_visibility="collapsed",
        key="page_navigation",
    )

    st.session_state.page = selected_page

    st.markdown("---")
    st.markdown("""
    <div style="
        background:#5b4034;
        border:1px solid #795c4c;
        border-radius:18px;
        padding:18px 14px;
        text-align:center;
        margin-top:20px;">
        <div style="font-size:28px;">🌱</div>
        <div style="font-size:19px;font-style:italic;font-weight:700;">
            Small steps<br>lead to<br>big results
        </div>
        <div style="font-size:22px;margin-top:8px;">🤎</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- HOME PAGE ----------------
if st.session_state.page == "Home":
    # Optional separate robot illustration: keep robot.jpg beside app.py.
    robot_path = Path("robot.jpg")

    if robot_path.exists():
        robot_html = (
            '<img src="data:image/jpeg;base64,'
            + base64.b64encode(robot_path.read_bytes()).decode("utf-8")
            + '" alt="Friendly study robot">'
        )
    else:
        robot_html = (
            '<div style="font-size:115px;text-align:center;'
            'min-width:150px;">🤖</div>'
        )

    st.markdown(f"""
    <div class="hero">
        <div>
            <h1>Hello there! 👋</h1>
            <h3>Your AI-powered study companion</h3>
            <p>
                Ask questions, summarize notes, plan your revision,<br>
                and test your knowledge — all in one place.
            </p>
        </div>
        {robot_html}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## What would you like to do today?")

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    cards = [
        (
            col1, "card-blue", "💬", "Ask AI Agent",
            "Get answers, search the web, calculate, or read files.",
        ),
        (
            col2, "card-green", "📖", "Summarize Notes",
            "Turn your notes into simple summaries.",
        ),
        (
            col3, "card-purple", "🗓️", "Revision Planner",
            "Create a personalized study plan.",
        ),
        (
            col4, "card-peach", "❓", "Generate Quiz",
            "Test your knowledge and get instant feedback.",
        ),
    ]

    for col, color, emoji, title, description in cards:
        with col:
            st.markdown(f"""
            <div class="feature-card {color}">
                <div class="emoji">{emoji}</div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

            st.button(
                "Explore →",
                key=f"open_{title}",
                use_container_width=True,
                on_click=navigate_to,
                args=(title,),
            )

    st.markdown("""
    <div class="tips">
        <h3>💡 Quick Tips</h3>
        <p>• Use the AI Agent for research, calculations, or file reading.</p>
        <p>• Turn your study notes into clear, easy summaries.</p>
        <p>• Plan your revision and practise with quizzes.</p>
        <div style="text-align:right;font-size:20px;
                    font-weight:800;color:#916751;">
            You can do it! ♡
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- ASK AI AGENT ----------------
elif st.session_state.page == "Ask AI Agent":
    st.title("💬 Ask AI Agent")
    st.write("Have a question? Let's figure it out together.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Type your question here...")

    if question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": question,
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = str(student_agent.run(question))
                    st.markdown(answer)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                    })
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    if st.button("Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()


# ---------------- SUMMARIZE NOTES ----------------
elif st.session_state.page == "Summarize Notes":
    st.title("📖 Summarize Notes")
    st.write("Make your study material easier to understand.")

    notes = st.text_area(
        "Paste your notes here",
        height=250,
        placeholder="Paste your chapter notes or study material...",
    )

    summary_style = st.selectbox(
        "Choose your summary style",
        [
            "Simple and easy to understand",
            "Short bullet points",
            "Exam revision notes",
            "Detailed summary",
        ],
    )

    if st.button("Create my summary", use_container_width=True):
        if not notes.strip():
            st.warning("Please enter some notes first.")
        else:
            prompt = f"""
Summarize the following study notes.
Style: {summary_style}
Use clear, student-friendly language.
Keep the information accurate and organized.

Notes:
{notes}
"""
            with st.spinner("Preparing your summary..."):
                try:
                    response = gemini_model.generate([
                        ChatMessage(role="user", content=prompt)
                    ])
                    st.markdown("### Your summary")
                    st.markdown(get_response_text(response))
                except Exception as e:
                    st.error(f"Could not create the summary: {e}")


# ---------------- REVISION PLANNER ----------------

elif st.session_state.page == "Revision Planner":
    st.title("🗓️ Revision Planner")
    st.write("Break your study topics into manageable daily goals.")

    # Keep the planner content at a comfortable width
    with st.container():
        topics = st.text_area(
            "What would you like to study?",
            placeholder="Example: Python, DBMS, Artificial Intelligence",
            height=130,
            key="revision_topics",
        )

        days = st.number_input(
            "How many days do you have?",
            min_value=1,
            max_value=90,
            value=5,
            step=1,
            key="revision_days",
        )

        create_plan = st.button(
            "Create my study plan",
            use_container_width=True,
            key="create_revision_plan_button",
        )

    if create_plan:
        if not topics.strip():
            st.warning("Please enter at least one topic.")
        else:
            with st.spinner("Making your study plan..."):
                try:
                    plan = create_revision_plan(
                        topics=topics.strip(),
                        days=int(days),
                    )

                    st.markdown("---")
                    st.markdown("## 📚 Your Study Plan")

                    if isinstance(plan, str):
                      import re

                      # Split the plan wherever a new day begins
                      formatted_plan = re.sub(
                         r"\s*(day\s*\d+\s*[:\-])",
                         r"\n\n### \1",
                         plan,
                        flags=re.IGNORECASE,
                         ).strip()

                      st.markdown(formatted_plan)
                    else:
                      st.write(plan)

                except: 
                    print("Could not generate revision plan !!")




# ---------------- GENERATE QUIZ ----------------
elif st.session_state.page == "Generate Quiz":
    st.title("✏️ Generate Quiz")
    st.write("A little practice can make a big difference!")

    topic = st.text_input(
        "Which topic would you like to practise?",
        placeholder="Example: Python functions",
        key="quiz_topic_input",
    )
    number_of_questions = st.selectbox(
        "Number of questions", [5, 10, 15], key="quiz_question_count"
    )

    if st.button("Create my quiz", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            prompt = f"""Create exactly {number_of_questions} multiple-choice questions about: {topic.strip()}.
                        Return ONLY a valid JSON array, with no Markdown fences or introduction.
                        Each item must have these keys: question, A, B, C, D, answer.
                        The values for A, B, C, and D are the option text. The answer value must be one letter: A, B, C, or D.
                        Example: [{{"question":"What is 2+2?","A":"3","B":"4","C":"5","D":"6","answer":"B"}}]
                        Make every question relevant, accurate, and distinct. Include exactly {number_of_questions} items.
                        """
            
            with st.spinner("Preparing your quiz..."):
                try:
                    response = gemini_model.generate([
                        ChatMessage(role="user", content=prompt)
                    ])
                    quiz_text = get_response_text(response).strip()
                    # Remove optional Markdown fences if the model adds them.
                    quiz_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", quiz_text, flags=re.IGNORECASE)
                    match = re.search(r"\[.*\]", quiz_text, flags=re.DOTALL)
                    if match:
                        quiz_text = match.group(0)
                    parsed = json.loads(quiz_text)
                    if not isinstance(parsed, list):
                        raise ValueError("The AI response was not a JSON list.")
                    questions = []
                    for item in parsed:
                        if not isinstance(item, dict):
                            continue
                        answer = str(item.get("answer", "")).strip().upper()
                        if all(k in item for k in ("question", "A", "B", "C", "D")) and answer in "ABCD" and len(answer) == 1:
                            questions.append({
                                "question": str(item["question"]).strip(),
                                "options": [(letter, str(item[letter]).strip()) for letter in "ABCD"],
                                "answer": answer,
                            })
                    if not questions:
                        st.error("The AI response could not be converted into questions. Please try again.")
                        with st.expander("View raw AI response"):
                            st.code(get_response_text(response))
                    else:
                        st.session_state.quiz = json.dumps(questions)
                        st.session_state.quiz_topic = topic.strip()
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_score = None
                        st.rerun()
                except Exception as e:
                    st.error(f"Could not generate the quiz: {e}")

    # Render a saved quiz only on the Generate Quiz page.
    if st.session_state.quiz:
        try:
            questions = json.loads(st.session_state.quiz)
        except (TypeError, json.JSONDecodeError):
            questions = []

        if questions:
            st.markdown(f"### Quiz: {st.session_state.quiz_topic}")
            st.caption(f"{len(questions)} questions generated.")

            if not st.session_state.quiz_submitted:
                with st.form("quiz_form"):
                    chosen_answers = {}
                    for i, question in enumerate(questions):
                        st.markdown(f"**Q{i + 1}. {question['question']}**")
                        chosen_answers[i] = st.radio(
                            "Choose an answer",
                            [f"{letter}) {text}" for letter, text in question["options"]],
                            index=None,
                            key=f"quiz_answer_{i}",
                        )
                        st.divider()
                    submitted = st.form_submit_button("Check my answers", use_container_width=True)

                if submitted:
                    unanswered = [i + 1 for i, value in chosen_answers.items() if value is None]
                    if unanswered:
                        st.warning("Please answer every question before submitting.")
                    else:
                        correct = 0
                        results = []
                        for i, question in enumerate(questions):
                            selected_letter = chosen_answers[i].split(")", 1)[0]
                            is_correct = selected_letter == question["answer"]
                            correct += int(is_correct)
                            results.append({
                                "question": question["question"],
                                "selected": selected_letter,
                                "correct": question["answer"],
                                "is_correct": is_correct,
                            })
                        st.session_state.quiz_score = (correct, len(questions), results)
                        st.session_state.quiz_submitted = True
                        st.rerun()

            if st.session_state.quiz_submitted and st.session_state.quiz_score:
                correct, total, results = st.session_state.quiz_score
                percentage = correct / total * 100 if total else 0
                st.markdown("### Your results")
                col1, col2 = st.columns(2)
                col1.metric("Correct answers", f"{correct}/{total}")
                col2.metric("Your score", f"{percentage:.0f}%")
                st.progress(percentage / 100)
                if percentage >= 80:
                    st.success("Wonderful work! Keep it up 🌟")
                elif percentage >= 50:
                    st.info("Good effort! A little more practice will help.")
                else:
                    st.info("Keep practising. Every attempt helps you learn!")
                st.markdown("### Answer Review")
                for i, result in enumerate(results):
                    st.markdown(f"**Q{i + 1}. {result['question']}**")
                    if result["is_correct"]:
                        st.success(f"Your answer: {result['selected']} — Correct!")
                    else:
                        st.error(f"Your answer: {result['selected']} — Incorrect")
                        st.info(f"Correct answer: {result['correct']}")
                if st.button("Generate Another Quiz", use_container_width=True):
                    st.session_state.quiz = None
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = None
                    st.session_state.quiz_topic = ""
                    st.rerun()


# ---------------- SETTINGS ----------------
elif st.session_state.page == "Settings":
    st.title("⚙️ Settings")
    st.write("Make your study space feel right for you.")

    st.markdown("### About StudyPilot-AI")
    st.write(
        "Your friendly study companion for asking questions, "
        "summarizing notes, planning revision, and practising quizzes."
    )

    st.markdown("### Conversation")
    st.write(
        f"Messages in the current conversation: "
        f"{len(st.session_state.chat_history)}"
    )

    if st.button("Clear chat history"):
        st.session_state.chat_history = []
        st.success("Chat history cleared.")
