import ast

class AIReview(ast.NodeVisitor):

    def __init__(self):
        self.defined = set()
        self.used = set()

    
    # IMPORT TRACKING
    

    def visit_Import(self, node): 
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    
    # VARIABLE TRACKING
    

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store): 
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

 
    # INFINITE LOOP DETECTION
    def visit_While(self, node):
        # Check if condition is always True
        is_infinite_condition = False

        # Case 1: while True
        if isinstance(node.test, ast.Constant) and node.test.value == True:
            is_infinite_condition = True

        # Case 2: while 1
        if isinstance(node.test, ast.Constant) and node.test.value == 1:
            is_infinite_condition = True

        if is_infinite_condition:
            has_break = False

            # Check if loop contains break
            for child in ast.walk(node):
                if isinstance(child, ast.Break):
                    has_break = True
                    break

            if not has_break:
                print(f"Possible Infinite Loop detected at line {node.lineno}")

        self.generic_visit(node)

    
    # UNUSED REPORT
    

    def reportOfUnused(self):
        unused = self.defined - self.used
        print('--- AI Review Report ---')
        if not unused:
            print("Everything is used! Good job bro!")
        for item in unused:
            print(f'Unused Item : {item}')



# SAMPLE CODE


code = '''
import os 
import sys
from datetime import datetime, timedelta

score = 100
print(score)

while True:
    print("Running forever")
'''

tree = ast.parse(code)
review = AIReview()
review.visit(tree)
review.reportOfUnused()