import os
import sys
import ast

def check_file(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read(), filename=file_path)

    # Check for module-level docstring
    if not tree.body or not isinstance(tree.body[0], ast.Expr) or not isinstance(tree.body[0].value, ast.Str):
        print(f"File {file_path} is missing a module-level docstring")

    # Check for class and function docstrings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.body or not isinstance(node.body[0], ast.Expr) or not isinstance(node.body[0].value, ast.Str):
                print(f"Function/Class {node.name} in file {file_path} is missing a docstring")

def walk_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                check_file(os.path.join(root, file))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Invalid directory path")
        sys.exit(1)

    walk_directory(directory)

