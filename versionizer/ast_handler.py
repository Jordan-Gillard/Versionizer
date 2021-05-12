import ast
from collections import defaultdict
from typing import Any, Dict

import astor

from versionizer.function_node import FunctionNode


class ASTHandler(ast.NodeTransformer):
    """
    When initialized with a Python file, this class will parse the AST for that file
    and note all the different functions, as well as build a dictionary detailing
    which functions one function directly relies on.
    """

    def __init__(self, file: str):
        super().__init__()
        self.file: str = file
        self._nodes: Dict[FunctionNode, FunctionNode] = {}
        self._curr_func: list = []
        self._function_dependents = defaultdict(set)
        compiled_ast = astor.parse_file(self.file)
        self.visit(compiled_ast)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self._curr_func.append(node.name)
        self.generic_visit(node)
        func_node = FunctionNode(node)
        self._nodes[func_node] = func_node
        self._curr_func.pop()

    def visit_Call(self, node: ast.Call) -> Any:
        self._function_dependents[node.func.id].add(self._curr_func[-1])
        self.generic_visit(node)

    def get_function_nodes(self) -> Dict[FunctionNode, FunctionNode]:
        return self._nodes

    def get_function_dependents(self):
        return self._function_dependents
