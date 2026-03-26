import ast


class AIReview(ast.NodeVisitor):

    def __init__(self):
        self.defined = set()
        self.used = set()
        self.infinite_loops = []

    # ---------------- IMPORT TRACKING ---------------- #

    def visit_Import(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    # ---------------- VARIABLE TRACKING ---------------- #

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

        self.generic_visit(node)

    # ---------------- INFINITE LOOP DETECTION ---------------- #

    def visit_While(self, node):

        is_infinite_condition = False

        # Case 1: while True
        if isinstance(node.test, ast.Constant) and node.test.value == True:
            is_infinite_condition = True

        # Case 2: while 1
        if isinstance(node.test, ast.Constant) and node.test.value == 1:
            is_infinite_condition = True

        if is_infinite_condition:
            has_break = False

            for child in ast.walk(node):
                if isinstance(child, ast.Break):
                    has_break = True
                    break

            if not has_break:
                self.infinite_loops.append(node.lineno)

        self.generic_visit(node)


# ---------------- REPORT FUNCTION ---------------- #

def report_unused(tree):

    review = AIReview()
    review.visit(tree)

    unused = review.defined - review.used

    return {
        "unused_variables": list(unused),
        "infinite_loops": review.infinite_loops
    }