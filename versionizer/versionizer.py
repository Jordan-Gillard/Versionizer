import logging
import os
from typing import Optional, Set

from versionizer.ast_differ import ASTDiffer
from versionizer.ast_handler import ASTHandler
from versionizer.automated_test_executor import AutomatedTestExecutor
from versionizer.automated_test_generator import AutomatedTestGenerator
from versionizer.function_node import FunctionNode
from versionizer.git_handler import GitHandler
from versionizer.parsed_ast_builder import ParsedASTBuilder


class Versionizer:
    def __init__(self, project_path: str,
                 first_commit: str,
                 output_path: Optional[str] = None,
                 second_commit: Optional[str] = None,
                 module: str = "",
                 algorithm="WHOLE_SUITE",
                 generate_tests=True,
                 run_tests=True):
        self.project_path = project_path
        self.module = module
        if not output_path:
            self.output_path = project_path
        else:
            self.output_path = output_path
        self.first_commit = first_commit
        self.second_commit = second_commit
        self._validate_algorithm(algorithm)
        self.algorithm = algorithm
        self.generate_tests = generate_tests
        self.run_tests = run_tests
        self.test_generator = AutomatedTestGenerator(project_path, output_path,
                                                     algorithm, module)
        self.git_handler = GitHandler(self.first_commit, self.second_commit)

    @staticmethod
    def _validate_algorithm(algorithm):
        # TODO: Should algorithm validation be done in the AutomatedTestGenerator?
        accepted_algorithms = ["RANDOM", "MOSA", "RANDOM_SEARCH", "WHOLE_SUITE"]
        if algorithm not in accepted_algorithms:
            raise ValueError(f"Algorithms must be one of {', '.join(algorithm)}.")

    def run(self):
        self.git_handler.stash_changes_if_necessary()
        try:
            # Handle working with a single file
            if self.module:
                self._run_for_file(self.project_path, self.module)
            # Handle working with an entire directory
            else:
                for dirpath, dirnames, filenames in os.walk(self.project_path):
                    for file in filenames:
                        if file.endswith(
                                ".py") and "test" not in file and "init" not in file:
                            self._run_for_file(self.project_path, file)

        except Exception as e:
            logging.error(e)
        finally:
            self.git_handler.return_to_head()
            self.git_handler.pop_stash_if_needed()

        if self.run_tests:
            AutomatedTestExecutor.run_tests(self.project_path)

    def _run_for_file(self, project_path, file):
        self.git_handler.checkout_first_commit()
        file_path_to_test = os.path.join(project_path, file)

        ast_handler_1 = ASTHandler(file_path_to_test)
        self.git_handler.checkout_second_commit()
        ast_handler_2 = ASTHandler(file_path_to_test)
        ast_differ = ASTDiffer(ast_handler_1, ast_handler_2)
        different_nodes: Set[FunctionNode] = ast_differ.get_changed_function_nodes()

        self.git_handler.checkout_first_commit()
        parsed_ast_builder: ParsedASTBuilder = ParsedASTBuilder(file_path_to_test,
                                                                different_nodes,
                                                                ast_handler_1.get_function_dependents())
        parsed_ast_builder.build_source()

        if self.generate_tests:
            self.test_generator.generate_tests()

        test_file_name = "test_" + file
        test_file_path = os.path.join(project_path, test_file_name)
        with open(test_file_path, "r+") as f:
            test_file_lines = f.readlines()

        self.git_handler.return_to_head()
        with open(test_file_path, "w") as f:
            f.writelines(test_file_lines)
