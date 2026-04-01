import re

def detect_issues(code: str):
    unused_variables = []
    infinite_loops = []

    lines = code.split("\n")

    # 🔴 Detect infinite loops (C, C++, Java, JS, Python)
    for i, line in enumerate(lines):
        line_clean = line.strip().lower().replace(" ", "")

        if "while(true)" in line_clean:
            infinite_loops.append(i + 1)

        if "for(;;)" in line_clean:
            infinite_loops.append(i + 1)

    # 🔴 Detect variable declarations (C-style + others)
    variables = re.findall(
        r'\b(int|float|double|char|long|short|string|bool|var|let|const)\s+(\w+)',
        code
    )

    for var_type, var_name in variables:
        # Count occurrences (basic unused detection)
        if code.count(var_name) == 1:
            unused_variables.append(var_name)

    return {
        "unused_variables": list(set(unused_variables)),
        "infinite_loops": list(set(infinite_loops))
    }