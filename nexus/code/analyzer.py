"""
Project NEXUS
Code Analyzer
"""

import ast


class CodeAnalyzer:
    """Analyzes Python AST."""

    def analyze(self, tree: ast.AST) -> dict:
        classes = []
        functions = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.append(module)

        return {
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "class_count": len(classes),
            "function_count": len(functions),
            "import_count": len(imports),
        }