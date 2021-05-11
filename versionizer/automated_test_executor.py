import os

from versionizer.utils import print_bright_blue


class AutomatedTestExecutor:
    # TODO: This can probably just be a function
    """
    This class runs all tests in a given location. This location can be a directory,
    in which case it will run all test files within, or a file.
    """

    @staticmethod
    def run_tests(test_location):
        print_bright_blue("Beginning test run.")
        print(f"pytest --quiet --color=yes {test_location}")
        os.system(f"pytest --quiet --color=yes {test_location}")
