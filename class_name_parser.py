"""
\n This script parses Python files in a given directory (and its subdirectories),
\n extracts the names of all classes and functions along with their comments (if any),
\n and prints the results in a structured format.
"""
import ast
import os
import re


class ClassNameParser:
    """
    \n Extracts the names of all classes and functions
    """

    def __init__(self, dir_path):
        """
        \n Initialize the ClassNameParser with the directory path to parse.
        """
        self.dir_path = dir_path

    def parse_python_file(self, file_path):
        """
        \n Parse a Python file and return its Abstract Syntax Tree (AST).
        \n Handle SyntaxError and general exceptions.
        """
        try:
            with open(file_path, "r", encoding='utf-8') as source:
                tree = ast.parse(source.read())
            return tree
        except IOError as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return None
        except SyntaxError as e:
            print(
                f"Syntax error in file {file_path} at line {e.lineno}: {e.text.strip()}")
            return None

    def get_classes_functions_and_comments(self, tree):
        """
        Extract classes and functions from the AST.
        """
        classes = [(
            node.name,
            re.sub(r'\s+', ' ', ast.get_docstring(node)) if ast.get_docstring(node) else None)
            for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [(
            node.name,
            re.sub(r'\s+', ' ', ast.get_docstring(node)) if ast.get_docstring(node) else None)
            for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return classes, functions

    def parse_directory(self):
        """
        \n Parse a directory and extract classes and functions from all .py files.
        \n Skip __init__.py files.
        """
        result = {}
        for root, _, files in os.walk(self.dir_path):
            for file in files:
                if file.endswith(".py") and not file == "__init__.py":
                    file_path = os.path.join(root, file)
                    tree = self.parse_python_file(file_path)
                    if tree is not None:
                        classes, functions = self.get_classes_functions_and_comments(
                            tree)
                        if classes or functions:  # Add the file only if it has classes or functions
                            result[file_path] = {
                                "classes": classes, "functions": functions}
        return result

    def print_parsed_data(self, parsed_data):
        """
        \n Print the parsed data in a structured format.
        """
        for file_path, data in parsed_data.items():
            print(f"\nFile: {file_path}")
            if data["classes"]:
                print("Classes:")
                for name, comment in data["classes"]:
                    print(
                        f"  {name}{' - ' + comment if comment else ''}")
            if data["functions"]:
                print("Functions:")
                for name, comment in data["functions"]:
                    print(
                        f"  {name}{' - ' + comment if comment else ''}")

    def run(self):
        """
        \n Run the parser and print the results.
        """
        parsed_data = self.parse_directory()
        self.print_parsed_data(parsed_data)
        print("\nAll done!")


if __name__ == '__main__':
    parser = ClassNameParser("app")  # Replace "app" with your directory path
    parser.run()
