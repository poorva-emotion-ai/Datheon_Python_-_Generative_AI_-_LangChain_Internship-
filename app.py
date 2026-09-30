import streamlit as st
from agent import student_agent,gemini_model
from smolagents import ChatMessage
from tools import create_revision_plan,evaluate_answer

#
# Parse_quiz 
#

def parse_quiz(quiz_text):

    questions = []

    blocks = quiz_text.split("QUESTION")

    for block in blocks[1:]:

        lines = block.strip().split("\n")

        question = ""
        options = {}
        answer = ""

        for line in lines:

            line = line.strip()

            if line.startswith("Question:"):
                question = line.replace("Question:", "").strip()

            elif line.startswith("A:"):
                options["A"] = line.replace("A:", "").strip()

            elif line.startswith("B:"):
                options["B"] = line.replace("B:", "").strip()

            elif line.startswith("C:"):
                options["C"] = line.replace("C:", "").strip()

            elif line.startswith("D:"):
                options["D"] = line.replace("D:", "").strip()

            elif line.startswith("ANSWER:"):
                answer = line.replace("ANSWER:", "").strip().upper()

        if question and len(options) == 4 and answer in options:

            questions.append({
                "question": question,
                "options": options,
                "answer": answer
            })

    return questions

# 
# Page Configuration
# 

st.set_page_config(
    page_title="AI Student Revision Agent",
    page_icon="🎓",
    layout="wide"
)

#
#Session state 
#

if "quiz"not in st.session_state:
    st.session_state.quiz=None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted=False
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score=None

# 
# Title
# 

st.title("🎓 AI Student Revision Agent")

st.write(
    "Your personal AI study assistant for revision planning, "
    "summaries, quizzes, and answer evaluation."
)

st.divider()


# 
# Sidebar
# 

st.sidebar.title("📚 Study Assistant")

feature = st.sidebar.selectbox(
    "Choose a feature",
    [
        "💬 Ask AI Agent",
        "📚 Summarize Notes",
        "📅 Revision Planner",
        "📝 Generate Quiz"
    ]
)


# 
# 1. ASK AI AGENT
# 
if feature == "💬 Ask AI Agent":

    st.header("💬 Ask Your AI Study Assistant")

    question = st.text_area(
        "What do you want to know?",
        placeholder="Example: Explain CNN in simple words..."
    )

    if st.button("Ask Agent"):

        if question.strip():

            with st.spinner("🤖 Thinking..."):

                result = student_agent.run(question)

            st.subheader("🤖 Agent Response")
            st.write(result)

        else:

            st.warning("Please enter a question.")


# 
# 2. SUMMARIZE NOTES
# 

elif feature == "📚 Summarize Notes":

    st.header("📚 Summarize Your Notes")

    notes = st.text_area(
        "Paste your study material",
        height=300,
        placeholder="Paste your notes here..."
    )

    if st.button("Generate Summary"):

        if notes.strip():

            prompt = f"""
            Summarize the following study material into concise
            revision notes.

            Include:
            - Important definitions
            - Key concepts
            - Important points
            - Important formulas or facts, if present

            Keep the explanation simple and suitable for a student.

            Study material:

            {notes}

            """
            with st.spinner("📚 Creating your revision notes..."):
                response = gemini_model.generate([
                         ChatMessage(
                                        role="user",
                                        content=prompt
                                    )
                        ])

            result = response.content

            st.subheader("📖 Revision Notes")
            st.write(result)

        else:

            st.warning("Please paste your study material.")


# 
# 3. REVISION PLANNER
# 
elif feature == "📅 Revision Planner":

    st.header("📅 Create Your Revision Plan")

    topics = st.text_input(
        "Enter topics separated by commas",
        placeholder="CNN, RNN, LSTM, GRU"
    )

    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=30,
        value=4
    )

    if st.button("Create Plan"):

        if topics.strip():

            with st.spinner("📅 Creating your study plan..."):

                result = create_revision_plan(
                    topics=topics,
                    days=days
                )

            st.subheader("🗓️ Your Revision Plan")
          

            for line in result.split("\n"):
              st.write("📌 " + line)
            

        else:

            st.warning("Please enter your topics.")


# 
# 4. Generate QUIZ
#
elif feature == "📝 Generate Quiz":

    st.header("📝 Generate a Quiz")

    topic = st.text_input(
        "Enter a topic",
        placeholder="Example: OpenCV"
    )

    num_questions = st.number_input(
        "Number of questions",
        min_value=1,
        max_value=30,
        value=5
    )

    if st.button("🚀 Generate Quiz"):

        if topic.strip():

            with st.spinner("📝 Creating your quiz..."):

                response = gemini_model.generate([
                                ChatMessage(
                                    role="user",
                                    content=f"""
                                        Generate exactly {num_questions} multiple-choice questions
                                        about {topic}.

                                        Use EXACTLY this format:
                                        QUESTION 1:
                                        Question: <question>
                                        A: <option A>
                                        B: <option B>
                                        C: <option C>
                                        D: <option D>
                                        ANSWER: <A/B/C/D>

                                        QUESTION 2:
                                        Question: <question>
                                        A: <option A>
                                        B: <option B>
                                        C: <option C>
                                        D: <option D>
                                        ANSWER: <A/B/C/D>

                                        Continue until exactly {num_questions} questions.

                                        Rules:
                                            - Each question must have exactly four options.
                                            - Each question must have exactly one correct answer.
                                            - Do not add explanations.
                                            - Do not add extra text before or after the quiz.
                                        """
                                    )
                            ])


                quiz_text = response.content

                quiz = parse_quiz(str(quiz_text))

                if len(quiz) == num_questions:

                 st.session_state.quiz = quiz
                 st.session_state.quiz_submitted = False
                 st.session_state.quiz_score = None

                 st.success("🎉 Quiz generated!")

                else:

                 st.error(
                    "The quiz could not be generated correctly. "
                    "Please try again."
                )

        else:

            st.warning("Please enter a topic.")

# Display quiz


if st.session_state.quiz:

    st.divider()

    st.subheader("🧠 Your Quiz")

    student_answers = []

    for i, q in enumerate(st.session_state.quiz):

        st.write(f"### Question {i + 1}")
        st.write(q["question"])

        answer = st.radio(
            "Choose your answer:",
            options=["A", "B", "C", "D"],
            format_func=lambda x: f"{x}. {q['options'][x]}",
            key=f"question_{i}"
        )

        student_answers.append(answer)

    if st.button("📊 Submit Quiz"):

        correct_answers = [
            q["answer"]
            for q in st.session_state.quiz
        ]

        student_answer_string = ",".join(student_answers)
        correct_answer_string = ",".join(correct_answers)

        result = evaluate_answer(
            correct_answer=correct_answer_string,
            student_answer=student_answer_string
        )

        st.session_state.quiz_score = result
        st.session_state.quiz_submitted = True

    #
    # Reveal answer after submittion 
    #


    if st.session_state.quiz_submitted:

        st.divider()

        st.subheader("🏆 Quiz Result")

        st.write(st.session_state.quiz_score)

        st.subheader("📖 Answer Review")

        for i, q in enumerate(st.session_state.quiz):

            st.write(f"**Question {i + 1}:** {q['question']}")

            st.write(
            f"Your answer: "
            f"{st.session_state.get(f'question_{i}')}"
            )

            st.write(
            f"Correct answer: **{q['answer']}**"
            )


    