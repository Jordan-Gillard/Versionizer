from typing import Set

import astor

from versionizer.ast_handler import ASTHandler
from versionizer.function_node import FunctionNode


class ASTDiffer:

    def __init__(self, ast_handler_1: ASTHandler, ast_handler_2: ASTHandler):
        super().__init__()
        self.ast_handler_1: ASTHandler = ast_handler_1
        self.ast_handler_2: ASTHandler = ast_handler_2

    @staticmethod
    def _functions_have_not_changed(node1: FunctionNode, node2: FunctionNode):
        return astor.dump_tree(node1.body) == astor.dump_tree(node2.body)

    def get_changed_function_nodes(self) -> Set[FunctionNode]:
        nodes1 = self.ast_handler_1.get_function_nodes()
        nodes2 = self.ast_handler_2.get_function_nodes()
        same_func_nodes = nodes1.keys() & nodes2.keys()
        return {n for n in same_func_nodes if
                not self._functions_have_not_changed(nodes1[n], nodes2[n])}
