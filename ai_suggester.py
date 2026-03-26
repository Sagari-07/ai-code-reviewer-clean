from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

prompt = PromptTemplate(
    input_variables=["code_string"],
    template="""
You are a strict Python code reviewer.

You MUST follow this format EXACTLY and ONLY ONCE.

DO NOT repeat anything.
DO NOT add extra sections.
DO NOT include "Refactored Code".

FORMAT:

🔴 Syntax Errors
- ...

🟡 Code Issues
- Unused imports: ...
- Bad practices: ...
- Naming issues: ...
- PEP8 issues: ...

🟢 Suggestions
- ...

📊 Complexity
- Time Complexity: ...
- Space Complexity: ...

✅ Corrected Code
```python
# Always provide working improved code

Code:
{code_string}
"""
)

def get_ai_suggestion(code_string):
    try:
        formatted_prompt = prompt.format(code_string=code_string)
        result = model.invoke(formatted_prompt)

        output = result.content.strip()

        # 🔥 REMOVE DUPLICATE BLOCKS
        if "🔴 Syntax Errors" in output:
            output = output.split("🔴 Syntax Errors", 1)[1]
            output = "🔴 Syntax Errors" + output

        # 🔥 EXTRACT CORRECTED CODE
        corrected_code = ""
        if "```python" in output:
            parts = output.split("```python")
            if len(parts) > 1:
                corrected_code = parts[1].split("```")[0].strip()

        # 🔥 REMOVE CODE BLOCK FROM MAIN TEXT
        clean_text = output.split("```python")[0].strip()

        return {
            "text": clean_text,
            "corrected_code": corrected_code
        }

    except Exception as e:
        return {
            "text": f"Error: {str(e)}",
            "corrected_code": ""
        }