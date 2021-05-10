import ast
from collections import defaultdict

import astor
from typing import Any, Dict

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
        self.nodes: Dict[FunctionNode, FunctionNode] = {}
        self.curr_func = None
        self.node_dependents = defaultdict(set)
        compiled_ast = astor.parse_file(self.file)
        self.visit(compiled_ast)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.generic_visit(node)
        func_node = FunctionNode(node)
        self.nodes[func_node] = func_node

    def visit_Call(self, node: ast.Call) -> Any:
        self.node_dependents[self.curr_func].add(node.func.id)
        self.generic_visit(node)

    def get_all_function_nodes(self) -> Dict[FunctionNode, FunctionNode]:
        return self.nodes
