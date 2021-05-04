import ast

import astor
from typing import Any, Dict

from versionizer.graph_node import GraphNode


class ASTHandler(ast.NodeTransformer):
    def __init__(self, file: str):
        super().__init__()
        self.file: str = file
        self.nodes: Dict[GraphNode, GraphNode] = {}
        compiled_ast = astor.parse_file(self.file)
        self.visit(compiled_ast)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.generic_visit(node)
        gNode = GraphNode(node)
        self.nodes[gNode] = gNode

    def get_all_function_nodes(self) -> Dict[GraphNode, GraphNode]:
        return self.nodes
