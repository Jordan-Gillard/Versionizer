import logging
import os
from argparse import Namespace


class AutomatedTestExecutor:
    def __init__(self, namespace: Namespace):
        self.namespace = namespace

    def _create_init_file_in_test_dir_if_not_exists(self):
        init_file_loc = os.path.join(self.namespace.output_path, '__init__.py')
        if not os.path.exists(init_file_loc):
            open(init_file_loc, 'a').close()

    def _check_for_versions(self):
        if not self.namespace.previous_version and not self.namespace.run_tests:
            logging.info("Previous version and new version are not set. Versionizer"
                         " will run tests with the latest version of the library.")

    def run_tests(self):
        self._create_init_file_in_test_dir_if_not_exists()
        os.system(f"pytest {self.namespace.output_path}")
