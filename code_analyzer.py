
from language_detector import detect_language
from ai_suggester import get_ai_suggestion

from universal_detector import detect_issues

def analyze_code_pipeline(code, language=None):

    if not language or language.lower() == "auto":
        language = detect_language(code)
    else:
        language = language.lower()

    # ✅ UNIVERSAL DETECTION (for ALL languages)
    universal_errors = detect_issues(code)

    # -------- PYTHON EXTRA -------- #
    if language == "python":
        from code_parser import parse_code
        from error_detector import report_unused

        syntax_result = parse_code(code)

        if not syntax_result["success"]:
            return {
                "status": "error",
                "unused_variables": [],
                "infinite_loops": [],
                "ai_suggestion": f"🔴 Syntax Errors:\n{syntax_result['error']}",
                "corrected_code": ""
            }

        tree = syntax_result["tree"]
        python_errors = report_unused(tree)

        # merge results
        unused_vars = list(set(universal_errors["unused_variables"] + python_errors.get("unused_variables", [])))
        loops = list(set(universal_errors["infinite_loops"] + python_errors.get("infinite_loops", [])))

    else:
        unused_vars = universal_errors["unused_variables"]
        loops = universal_errors["infinite_loops"]

    ai_result = get_ai_suggestion(code, language)

    return {
        "status": "success",
        "unused_variables": unused_vars,
        "infinite_loops": loops,
        "ai_suggestion": ai_result.get("text", ""),
        "corrected_code": ai_result.get("corrected_code", "")
    }