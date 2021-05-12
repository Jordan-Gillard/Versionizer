#!/usr/bin/env python3
import argparse
import logging
import os
from typing import Set

from versionizer.ast_differ import ASTDiffer
from versionizer.ast_handler import ASTHandler
from versionizer.automated_test_executor import AutomatedTestExecutor
from versionizer.automated_test_generator import AutomatedTestGenerator
from versionizer.function_node import FunctionNode
from versionizer.git_handler import GitHandler
from versionizer.parsed_ast_builder import ParsedASTBuilder
from versionizer.utils import print_banner

parser = argparse.ArgumentParser(
    description="Automatically generate test cases to ensure the correctness of "
                "changed code.",
)

parser.add_argument(
    "--project-path",
    help="The directory which contains the python module. If the module argument is not"
         " specified, Versionizer will generate tests for all non-test Python files in"
         " this directory.",
    required=True
)


parser.add_argument(
    "--git-repo",
    help="The location of the Git repository for the project under test. If not "
         "provided, Versionizer will default to it's own repository and assume you're"
         "testing it on itself or sample directories.",
    required=False,
)


parser.add_argument(
    "-m",
    "--module",
    help="The python file to generate tests for. If empty, Versionizer will generate "
         "tests for all files in the module.",
    required=False
)

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

parser.add_argument(
    "-r",
    "--run-tests",
    default=True,
    action='store_true',
    dest="run_tests",
)

parser.add_argument(
    "-dr",
    "--dont-run-tests",
    action='store_false',
    dest="run_tests",
)

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
    help="Specify which algorithm to use for test generation. Defaults to whole suite "
         "tests, similar to EvoSuite.",
    choices=["RANDOM", "MOSA", "RANDOM_SEARCH", "WHOLE_SUITE"],
)


def generate_tests(args):
    test_generator = AutomatedTestGenerator(args)
    test_generator.generate_tests()


def validate_args(args):
    if not args.run_tests and not args.generate_tests:
        parser.error(
            "Please specify whether you want Versionizer to generate or run tests.")
    if args.generate_tests and not args.previous_commit:
        parser.error("Must specify a previous commit to generate tests for.")


def run_for_file(project_path, file, git_handler, args):
    git_handler.checkout_first_commit()
    file_path_to_test = os.path.join(project_path, file)

    ast_handler_1 = ASTHandler(file_path_to_test)
    git_handler.checkout_second_commit()
    ast_handler_2 = ASTHandler(file_path_to_test)
    ast_differ = ASTDiffer(ast_handler_1, ast_handler_2)
    different_nodes: Set[FunctionNode] = ast_differ.get_changed_function_nodes()

    git_handler.checkout_first_commit()
    parsed_ast_builder: ParsedASTBuilder = ParsedASTBuilder(file_path_to_test,
                                                            different_nodes,
                                                            ast_handler_1.get_function_dependents())
    parsed_ast_builder.build_source()

    if args.generate_tests:
        generate_tests(args)

    test_file_name = "test_" + file
    test_file_path = os.path.join(project_path, test_file_name)
    with open(test_file_path, "r+") as f:
        test_file_lines = f.readlines()

    git_handler.return_to_head()
    with open(test_file_path, "w") as f:
        f.writelines(test_file_lines)


def main():
    args = parser.parse_args()
    args.output_path = args.project_path
    print_banner()
    validate_args(args)

    git_handler: GitHandler = GitHandler(args.previous_commit, args.current_commit)
    git_handler.stash_changes_if_necessary()
    try:
        # Handle working with a single file
        if args.module:
            run_for_file(args.project_path, args.module, git_handler, args)
        # Handle working with an entire directory
        else:
            for dirpath, dirnames, filenames in os.walk(args.project_path):
                for file in filenames:
                    if file.endswith(
                            ".py") and "test" not in file and "init" not in file:
                        run_for_file(args.project_path, file, git_handler, args)

    except Exception as e:
        logging.error(e)
    finally:
        git_handler.return_to_head()
        git_handler.pop_stash_if_needed()

    if args.run_tests:
        AutomatedTestExecutor.run_tests(args.project_path)


if __name__ == "__main__":
    main()
