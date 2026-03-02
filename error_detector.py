import ast

code = '''
import os
import sys
from datetime import datetime, timedelta

def short_function():
    print("This is short")

def long_function():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    v = 22
    w = 23
    x = 24
    y = 25
    z = 26
    aa = 27
    bb = 28
    cc = 29
    dd = 30
    ee = 31
    ff = 32
    gg = 33
    hh = 34
    ii = 35
    jj = 36
    kk = 37
    ll = 38
    mm = 39
    nn = 40
    oo = 41
'''

tree = ast.parse(code)


# IMPORT FINDER

class ImportFinder(ast.NodeVisitor):
    def visit_Import(self, node):
        for alias in node.names:
            print(f'Found import: {alias.name}')

    def visit_ImportFrom(self, node):
        print(f'Found import from: {node.module}')


# VARIABLE TRACKER


class VariableContextTracker(ast.NodeVisitor):
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            print(f"Variable '{node.id}' is being defined at line {node.lineno}")
        elif isinstance(node.ctx, ast.Load):
            print(f"Variable '{node.id}' is being used at line {node.lineno}")
        self.generic_visit(node)


# FUNCTION LENGTH CHECKER (PEP8)


class FunctionLengthChecker(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        start_line = node.lineno
        end_line = node.end_lineno

        function_length = end_line - start_line

        print(f"\nFunction '{node.name}' starts at line {start_line} and ends at line {end_line}")
        print(f"Function length: {function_length} lines")

        if function_length > 40:
            print(f"WARNING: Function '{node.name}' is too long (>{40} lines)")

        self.generic_visit(node)




ImportFinder().visit(tree)
VariableContextTracker().visit(tree)
FunctionLengthChecker().visit(tree)