import ast
from typing import Any

import astor

from tests.shared_functions import generate_temp_file_with_content
from versionizer.function_node import FunctionNode


def test_function_node():

    class TempAST(ast.NodeVisitor):
        def __init__(self):
            self.func_node = None

        def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
            self.func_node = FunctionNode(node)

    func = "def foo(a, b, *args, **kwargs):\n    return 1"
    for file in generate_temp_file_with_content(func):
        compiled_ast = astor.parse_file(file)
        temp_AST = TempAST()
        temp_AST.visit(compiled_ast)
        assert temp_AST.func_node.name == "foo"
        assert temp_AST.func_node.num_params == 2
        assert temp_AST.func_node.returns is None
