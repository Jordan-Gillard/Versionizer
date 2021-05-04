#!/usr/bin/env python3
import argparse
import os

from typing import Set

from versionizer.ast_differ import ASTDiffer
from versionizer.ast_handler import ASTHandler
from versionizer.automated_test_executor import AutomatedTestExecutor
from versionizer.automated_test_generator import AutomatedTestGenerator
from versionizer.git_handler import GitHandler
from versionizer.graph_node import GraphNode
from versionizer.parsed_ast_builder import ParsedASTBuilder
from versionizer.utils import print_banner

parser = argparse.ArgumentParser(
    description="Automatically generate test cases to ensure the correctness of migrate code.",
)
parser.add_argument(
    "-m",
    "--module",
    help="The python file to generate tests for.",
    required=True
)
parser.add_argument(
    "--project-path",
    help="The directory to generate tests for.",
    required=True
)
# TODO: user can either generate or run the tests, or both -> but not neither
parser.add_argument(
    "-gt"
    "--generate-tests",
    help="Generate tests.",
    action="store_true"
)
parser.add_argument(
    "-dgt"
    "--dont-generate-tests",
    dest="generate_tests",
    help="Don't generate tests. Use this if you only want to execute existing tests.",
    action='store_false',
)
# parser.set_defaults(generate_tests=True)
parser.add_argument(
    "-r",
    "--run-tests",
    action='store_true',
    dest="run_tests",
)
parser.add_argument(
    "-dr",
    "--dont-run-tests",
    action='store_false',
    dest="run_tests",
)
# parser.set_defaults(run_tests=True)

parser.add_argument(
    "-p",
    "--previous-commit",
    help="The commit containing the original version of code.",
    required=True,
)
parser.add_argument(
    "-c",
    "--current-commit",
    default=None,
    help="The commit of the new code. Defaults to the current commit if not specified.",
)

parser.add_argument(
    "--algorithm",
    default="WHOLE_SUITE",
    help="Specify which algorithm to use for test generation. Defaults to whole suite tests, similar to EvoSuite.",
    choices=["RANDOM", "MOSA", "RANDOM_SEARCH", "WHOLE_SUITE"],
)


def generate_tests(args):
    test_generator = AutomatedTestGenerator(args)
    test_generator.generate_tests()


def run_tests(args):
    test_executor = AutomatedTestExecutor(args)
    test_executor.run_tests()


def validate_args(args):
    if not args.run_tests and not args.generate_tests:
        parser.error(
            "Please specify whether you want Versionizer to generate or run tests.")
    if args.generate_tests and not args.previous_commit:
        parser.error("Must specify a previous commit to generate tests for.")


def main():
    args = parser.parse_args()
    validate_args(args)
    print_banner()
    git_handler: GitHandler = GitHandler(args.previous_commit, args.current_commit)
    git_handler.checkout_first_commit()

    file_path_to_test = os.path.join(args.project_path, args.module)

    ast_handler_1 = ASTHandler(file_path_to_test)
    git_handler.checkout_second_commit()
    ast_handler_2 = ASTHandler(file_path_to_test)
    ast_differ = ASTDiffer(ast_handler_1, ast_handler_2)
    different_nodes: Set[GraphNode] = ast_differ.get_changed_function_nodes()

    git_handler.checkout_first_commit()
    parsed_ast_builder: ParsedASTBuilder = ParsedASTBuilder(file_path_to_test,
                                                            different_nodes)
    parsed_ast_builder.build_source()

    if args.generate_tests:
        generate_tests(args)

    # Now we need to save the tests, go to the second commit, rewrite the file,
    # and run the tests
    # TODO: Make test saver class?
    test_file_name = "test_" + args.module
    test_file_path = os.path.join(args.project_path, test_file_name)
    test_file_lines = []
    with open(test_file_path, "r") as f:
        test_file_lines = f.readlines()

    git_handler.return_to_head()
    with open(test_file_path, "r") as f:
        f.writelines(test_file_lines)

    if args.run_tests:
        run_tests(args)




if __name__ == "__main__":
    main()
