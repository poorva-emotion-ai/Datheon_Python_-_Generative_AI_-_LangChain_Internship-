from agent import student_agent

print("Testing Quiz generation...")

result=student_agent.run(
      "generate 5 mcq question from the topic open cv."
      "Follow thw exact format given by quiz generator tool." 
)

print("\nQuiz output")
print(result)
