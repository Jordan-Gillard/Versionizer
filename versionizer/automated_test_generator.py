import os
from argparse import Namespace

import pynguin

from versionizer.utils import print_bright_blue


class AutomatedTestGenerator:
    """
    This class has functions to generate tests for a given file (aka module) or
    directory.
    """

    def __init__(self, namespace: Namespace):
        # TODO: Replace namespace with specific arguments. Namespace is confusing
        #  It could take a Pynguin Configuration object (dataclass), and thus
        #  replace the _get_config function.
        self.namespace = namespace

    @staticmethod
    def _clean_filename(file):
        return file.replace(".py", "")

    @staticmethod
    def _is_file(module):
        return os.path.isfile(module)

    def _get_test_files_in_dir(self, dir):
        return {f for f in os.listdir(dir) if "test_" in f or "_test" in f}

    def _run_pynguin_for_file(self, file):
        config = self._get_config(
            self.namespace.algorithm,
            self.namespace.project_path,
            self.namespace.output_path,
            file
        )
        pynguin.generator.set_configuration(config)
        pynguin.generator.run_pynguin()

    def _generate_all_tests_in_module(self):
        for path, _, files in os.walk(self.namespace.project_path):
            for file in files:
                filepath = os.path.join(path, file)
                if os.path.isfile(filepath) and file.endswith(
                        ".py") and "test" not in file:
                    file = self._clean_filename(file)
                    self._run_pynguin_for_file(file)

    def _generate_all_tests_for_file(self):
        file = self._clean_filename(self.namespace.module)
        self._run_pynguin_for_file(file)

    def generate_tests(self):
        print_bright_blue("Generating tests...")
        test_files_before = self._get_test_files_in_dir(self.namespace.project_path)
        if self.namespace.module:
            self._generate_all_tests_for_file()
        else:
            self._generate_all_tests_in_module()
        test_files_after = self._get_test_files_in_dir(self.namespace.project_path)
        for file in test_files_before.symmetric_difference(test_files_after):
            if 'test' in file:
                print_bright_blue(f"New test file: {file}")
        print_bright_blue("Done generating tests.")

    @staticmethod
    def _get_config(algorithm, project_path, output_path, module_name):
        config = pynguin.Configuration(algorithm, project_path, output_path,
                                       module_name)
        return config
