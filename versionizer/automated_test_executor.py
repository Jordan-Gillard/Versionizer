import os
from argparse import Namespace

from colorama import Fore, Style


class AutomatedTestExecutor:
    def __init__(self, namespace: Namespace):
        self.namespace = namespace

    def _create_init_file_in_test_dir_if_not_exists(self):
        init_file_loc = os.path.join(self.namespace.output_path, '__init__.py')
        if not os.path.exists(init_file_loc):
            open(init_file_loc, 'a').close()

    def _check_for_versions(self):
        if not self.namespace.previous_version and not self.namespace.new_version:
            print("Previous version and new version are not set. Versionizer"
                  " will run tests with the latest version of the library.")

    def _install_python_library(self, library, version=None):
        if version:
            os.system(f"pip install -q {library}=={version}")
        else:
            os.system(f"pip install -q {self.namespace.library}")

    def _run_tests_in_test_dir(self, test_dir):
        os.system(f"pytest --quiet {self.namespace.output_path}")

    def _run_tests_for_version(self, version):
        print(Style.BRIGHT + Fore.BLUE +
              f"Runnings tests with {self.namespace.library}:{version}")
        self._install_python_library(self.namespace.library,
                                     version)
        self._run_tests_in_test_dir(self.namespace.output_path)

    def _run_tests_for_latest_version(self):
        print(
            f"Running tests with latest version of {self.namespace.library}")
        self._install_python_library(self.namespace.library)
        self._run_tests_in_test_dir(self.namespace.output_path)

    def run_tests(self):
        self._create_init_file_in_test_dir_if_not_exists()
        self._check_for_versions()
        if self.namespace.previous_version:
            self._run_tests_for_version(self.namespace.previous_version)
        if self.namespace.new_version:
            self._run_tests_for_version(self.namespace.new_version)
        else:
            self._run_tests_for_latest_version()
