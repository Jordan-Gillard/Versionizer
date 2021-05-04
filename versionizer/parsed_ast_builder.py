import ast

import astor
from typing import Any, Set

from graph_node import GraphNode


class ParsedASTBuilder(ast.NodeTransformer):
    def __init__(self, file_name: str, nodes_to_keep: Set[GraphNode]):
        super().__init__()
        self.file_name: str = file_name
        self.nodes_to_keep: Set[GraphNode] = nodes_to_keep

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        g_node: GraphNode = GraphNode(node)
        if g_node in self.nodes_to_keep:
            return self.generic_visit(node)

    def build_source(self):
        original_ast = astor.parse_file(self.file_name)
        pruned_ast = self.visit(original_ast)
        with open(self.file_name, "w") as f:
            f.write(astor.to_source(pruned_ast))
        print(f"Wrote new source file to {self.file_name}")
