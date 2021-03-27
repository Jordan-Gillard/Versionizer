import os
from argparse import Namespace


class TestGenerator():
    def __init__(self, namespace: Namespace):
        self.namespace = namespace

    @staticmethod
    def _clean_filename(file):
        return file.replace(".py", "")

    def _generate_all_tests_in_module(self, commands):
        for root, _, files in os.walk(self.namespace.module):
            for file in files:
                filepath = os.path.join(root, file)
                if os.path.isfile(filepath) and file.endswith(".py"):
                    file = self._clean_filename(file)
                    commands.append(f"--module-name {root}.{file}")
                    os.system(" ".join(commands))
                    commands.pop()

    def _generate_all_tests_for_file(self, commands):
        file = self._clean_filename(self.namespace.file)
        commands.append(f"--module-name {file}")
        os.system(" ".join(commands))

    def generate_tests(self):
        # TODO: User prev version, new version, library
        commands = [
            "pynguin",
            f"--algorithm {self.namespace.algorithm}",
            f"--project-path ./",
            f"--output-path {self.namespace.output_path}"
        ]
        if self.namespace.module:
            self._generate_all_tests_in_module(commands)
        else:
            self._generate_all_tests_for_file(commands)
