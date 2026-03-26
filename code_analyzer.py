from code_parser import parse_code
from error_detector import report_unused
from ai_suggester import get_ai_suggestion


def analyze_code_pipeline(code):

    syntax_result = parse_code(code)

    if not syntax_result["success"]:
        return {
            "status": "error",
            "unused_variables": [],
            "infinite_loops": [],
            "ai_suggestion": f"Syntax Error:\n{syntax_result['error']}",
            "corrected_code": ""
        }

    tree = syntax_result["tree"]

    errors = report_unused(tree)

    ai_result = get_ai_suggestion(code)

    return {
        "status": "success",
        "unused_variables": errors.get("unused_variables", []),
        "infinite_loops": errors.get("infinite_loops", []),
        "ai_suggestion": ai_result.get("text", ""),
        "corrected_code": ai_result.get("corrected_code", "")
    }