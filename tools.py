from smolagents import tool 

# Creating tool for revision plan 

@tool

def create_revision_plan(topics:str,days:int)->str:
    """
    Create a revision plan for a given topic and number of days.

    Args:
        topics: The topic which needs to be revised.
        days: Total number of days available for revision.
    """

    topic_list= [topic.strip() for topic in topics.split(",")]

    plan=[]

    for i,topic in enumerate(topic_list):
     day =(i%days)+1
     plan.append(f"day {day}: revise {topic}")

    return "\n".join(plan)


# Creating tool for evaluating student's answer

@tool
def evaluate_answer(correct_answer:str, student_answer:str)->str:
   """
   Evaluate the student's answer and score them 

   Args:
       correct_answer: The correct answer to the question.
       student_answer: The student's answer to the question.
   """
   correct=[answer.strip().upper() for answer in correct_answer.split(",")]
   student=[answer.strip().upper() for answer in student_answer.split(",")]

   if len(correct)!=len(student):
      return" The number of answers provided by the student does not match the number of correct answers."

   score=sum(c==s for c,s in zip(correct,student))
   total=len(correct)
   percent=(score/total)*100

   return f"score: {score}/{total} \n({percent:.2f}%)"

