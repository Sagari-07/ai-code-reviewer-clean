from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

prompt = PromptTemplate(
    input_variables=["code_string", "language"],
    template="""
You are a strict {language} code reviewer.

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
- Style issues: ... (PEP8 for Python, standard conventions for others)

🟢 Suggestions
- ...

📊 Complexity
- Time Complexity: ...
- Space Complexity: ...

✅ Corrected Code
```{language}
# Always provide working improved code

Code:
{code_string}
"""
)


def get_ai_suggestion(code_string, language="python"):
    try:
        formatted_prompt = prompt.format(
            code_string=code_string,
            language=language
        )

        result = model.invoke(formatted_prompt)
        output = result.content.strip()

        if "🔴 Syntax Errors" in output:
            output = output.split("🔴 Syntax Errors", 1)[1]
            output = "🔴 Syntax Errors" + output

        corrected_code = ""
        if "```" in output:
            parts = output.split("```")
            if len(parts) > 1:
                corrected_code = parts[1].strip()

        clean_text = output.split("```")[0].strip()

        return {
            "text": clean_text,
            "corrected_code": corrected_code
        }

    except Exception as e:
        return {
            "text": f"Error: {str(e)}",
            "corrected_code": ""
        }