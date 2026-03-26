import ast

def parse_code(user_code):
    """
    Parses user code using Python AST.
    Returns AST tree and formatted code.
    """

    try:
        # Parse the code
        tree = ast.parse(user_code)

        # Format the code
        formatted_code = ast.unparse(tree)

        # Return results
        return {
            "success": True,
            "tree": tree,
            "formatted_code": formatted_code
        }

    except SyntaxError as e:
        return {
            "success": False,
            "error": str(e)
        }