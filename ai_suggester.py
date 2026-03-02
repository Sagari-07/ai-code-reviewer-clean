#Suggestion
#1. Add LLM sugesstion for syntax error case as well
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")
code_string = """
def add_numbers(a, b)
    result = a + b
    return result

print(add_numbers(5, 3))
"""

prompt = PromptTemplate(
    input_variables=["code_string"],
    template="""
You are an experienced coding teacher.
Generate suggestions based on the given code for the student.
Explain WHY you are suggesting each improvement.
Mention errors like syntax errors, time complexity, space complexity, unused imports, bad practices, and also error like naming convention as per pep8 guide line   etc.
Variables and functions → snake_case
Classes → PascalCase
Code:
{code_string}
"""
)

def get_ai_suggestion(code_string):
    formatted_prompt = prompt.format(code_string=code_string)
    result = model.invoke(formatted_prompt)
    print(result.content)



get_ai_suggestion(code_string)

