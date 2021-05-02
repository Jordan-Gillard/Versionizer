import ast
from typing import Any, Dict, Set

import astor

from versionizer.graph_node import GraphNode


class ASTDiffer(ast.NodeTransformer):
    def __init__(self, file1: str, file2: str):
        super().__init__()
        self.g_creator_1: GraphCreator = GraphCreator(file1)
        self.g_creator_2: GraphCreator = GraphCreator(file2)

    def _nodes_are_same(self, node1: GraphNode, node2: GraphNode):
        return astor.dump_tree(node1.body) == astor.dump_tree(node2.body)

    def get_changed_function_nodes(self) -> Set[GraphNode]:
        nodes1 = self.g_creator_1.get_all_function_nodes()
        nodes2 = self.g_creator_2.get_all_function_nodes()
        same_func_nodes = nodes1.keys() & nodes2.keys()
        return {n for n in same_func_nodes if
                not self._nodes_are_same(nodes1[n], nodes2[n])}


class GraphCreator(ast.NodeTransformer):
    def __init__(self, file: str):
        super().__init__()
        self.file: str = file
        self.nodes: Dict[GraphNode, GraphNode] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.generic_visit(node)
        gNode = GraphNode(node)
        self.nodes[gNode] = gNode

    def get_all_function_nodes(self) -> Dict[GraphNode, GraphNode]:
        compiled_ast = astor.parse_file(self.file)
        self.visit(compiled_ast)
        return self.nodes
