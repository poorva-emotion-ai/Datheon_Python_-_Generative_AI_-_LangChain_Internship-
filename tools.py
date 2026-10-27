from smolagents import tool 
import ast
import operator
from pathlib import Path
from smolagents import tool
from duckduckgo_search import DDGS



# Creating tool for revision plan 

@tool
def create_revision_plan(topics: str, days: int) -> str:
    """
    Create a revision plan with one task for each available day.

    Args:
        topics: Comma-separated list of subjects or topics to revise.
        days: Total number of days available for revision.
    """
    topic_list = [
        topic.strip()
        for topic in topics.split(",")
        if topic.strip()
    ]

    if not topic_list:
        return "Please enter at least one valid topic."

    if days < 1:
        return "The number of days must be at least 1."

    plan = []

    for i in range(days):
        topic = topic_list[i % len(topic_list)]
        plan.append(f"Day {i + 1}: Revise {topic}")

    return "\n\n".join(plan)



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

# Web Search
@tool
def web_search(query: str) -> str:
    """
    Search the web for information about a topic.

    Args:
        query: The topic or question to search for.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return "No web search results found."

        output = []
        for result in results:
            output.append(
                f"Title: {result.get('title', 'N/A')}\n"
                f"URL: {result.get('href', 'N/A')}\n"
                f"Summary: {result.get('body', 'N/A')}"
            )

        return "\n\n".join(output)

    except Exception as e:
        return f"Web search failed: {e}"


# Calculator
@tool
def calculator(expression: str) -> str:
    """
    Calculate a basic mathematical expression.

    Args:
        expression: A math expression, such as '25 * 4 + 10'.
    """
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.FloorDiv: operator.floordiv,
    }

    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = calculate(node.left)
            right = calculate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large.")

            result = operators[type(node.op)](left, right)

            if abs(result) > 10**15:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](calculate(node.operand))

        raise ValueError("Unsupported mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        return f"Result: {calculate(tree)}"
    except Exception as e:
        return f"Could not calculate expression: {e}"


# Tool 5: Local Text File Reader
@tool
def read_local_file(file_path: str) -> str:
    """
    Read a local TXT or Markdown file.

    Args:
        file_path: Path to an existing local .txt or .md file.
    """
    try:
        path = Path(file_path).expanduser().resolve()

        if path.suffix.lower() not in (".txt", ".md"):
            return "Only .txt and .md files are supported."

        if not path.is_file():
            return "File not found. Please check the file path."

        if path.stat().st_size > 1_000_000:
            return "File is too large. Maximum supported size is 1 MB."

        return path.read_text(encoding="utf-8")

    except Exception as e:
        return f"Could not read file: {e}"
