
from agent import student_agent

print("StudyPilot AI Agent")
print("Type 'exit' to quit.")

while True:
    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    try:
        answer = student_agent.run(question)
        print("\nAgent:", answer)
    except Exception as e:
        print("\nAgent error:", e)
