import ast

import astor
from typing import Any, Set

from versionizer.function_node import FunctionNode


class ParsedASTBuilder(ast.NodeTransformer):
    def __init__(self, file_name: str, nodes_to_keep: Set[FunctionNode], dependent_funcs: Set[str]):
        super().__init__()
        self.file_name: str = file_name
        self.nodes_to_keep: Set[FunctionNode] = nodes_to_keep
        self.dependent_funcs = dependent_funcs

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        g_node: FunctionNode = FunctionNode(node)
        if g_node in self.nodes_to_keep or g_node.name in self.dependent_funcs:
            return self.generic_visit(node)

    def build_source(self):
        original_ast = astor.parse_file(self.file_name)
        pruned_ast = self.visit(original_ast)
        # TODO: Need to figure out how to rebuild an entire module for testing
        #  Maybe we should just run the tool one time for each file?
        with open(self.file_name, "w") as f:
            f.write(astor.to_source(pruned_ast))
        print(f"Wrote new source file to {self.file_name}")
