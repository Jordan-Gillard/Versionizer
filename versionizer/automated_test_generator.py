import os
from argparse import Namespace


class AutomatedTestGenerator:
    def __init__(self, namespace: Namespace):
        self.namespace = namespace

    @staticmethod
    def _clean_filename(file):
        return file.replace(".py", "")

    @staticmethod
    def _is_file(module):
        return os.path.isfile(module)

    @staticmethod
    def _clean_path(path):
        return path.replace(os.path.sep, '.')

    def _generate_all_tests_in_module(self, commands):
        for path, _, files in os.walk(self.namespace.module):
            for file in files:
                filepath = os.path.join(path, file)
                if os.path.isfile(filepath) and file.endswith(".py"):
                    file = self._clean_filename(file)
                    clean_path = self._clean_path(path)
                    commands.append(f"--module-name {clean_path}.{file}")
                    os.system(" ".join(commands))
                    commands.pop()

    def _generate_all_tests_for_file(self, commands):
        file = self._clean_filename(self.namespace.module)
        clean_path = self._clean_path(file)
        commands.append(f"--module-name {clean_path}")
        os.system(" ".join(commands))

    def generate_tests(self):
        commands = [
            "pynguin",
            f"--algorithm {self.namespace.algorithm}",
            f"--project-path ./",
            f"--output-path {self.namespace.output_path}",
        ]
        if self._is_file(self.namespace.module):
            self._generate_all_tests_for_file(commands)
        else:
            self._generate_all_tests_in_module(commands)
