import ast

def parse_user_code(user_code):
    """
    Parses user code using Python AST
    Returns formatted version and AST structure
    """

    try:
        # Step 1: Parse code
        tree = ast.parse(user_code)

        

        # Step 2: Get formatted version
        formatted_code = ast.unparse(tree)

        # Step 3: Get AST dump (optional for debugging)
        ast_structure = ast.dump(tree, indent=2)

        # Step 4: Return results (do NOT print here)
        return {
            "success": True,
            "formatted_code": formatted_code,
            "ast_dump": ast_structure
        }

    except SyntaxError as e:
        return {
            "success": False,
            "error": str(e)
        }
# Example usage (for testing purposes only, remove in production)
if __name__ == "__main__":
    user_code = """def greet(name):
    return f"Hello, {name}!"
print(greet("Alice"))"""
    result = parse_user_code(user_code)
    if result["success"]:

        print("Formatted Code:")
        print(result["formatted_code"])
        print("\nAST Dump:")
        print(result["ast_dump"])
    else:
        print("Error parsing code:")
        print(result["error"])

