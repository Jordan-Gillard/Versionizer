import ast
from collections import defaultdict
from random import random
from typing import Any

import astor

from versionizer.ast_handler import ASTHandler
from versionizer.parsed_ast_builder import ParsedASTBuilder

print(random())


if __name__ == '__main__':
    # file = "sample_files/funcs.py"
    directory = "sample_dir"
    compiled = astor.parse_file(directory)
    print(astor.dump_tree(compiled))
    # TODO: You will need to check if youre messing with a file or a directory,
    #  and change behavior depending on which youre messing with.
    # handler = ASTHandler(directory)
    # nodes = handler.get_all_function_nodes()
    # dependents = handler.node_dependents
    # builder = ParsedASTBuilder(directory, set(nodes.keys()), dependents)
    # TODO: Need to figure out how to rebuild an entire module for testing
