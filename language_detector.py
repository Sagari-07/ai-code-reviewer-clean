def detect_language(code: str):
    code = code.strip()

    if "import java" in code or "public class" in code:
        return "java"
    elif "#include" in code:
        return "c"
    elif "console.log" in code or "function" in code:
        return "javascript"
    elif "def " in code or "import " in code:
        return "python"
    else:
        return "unknown"