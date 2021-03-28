#!/usr/bin/env python3
import argparse

from versionizer.automated_test_executor import AutomatedTestExecutor
from versionizer.automated_test_generator import AutomatedTestGenerator

parser = argparse.ArgumentParser(
    description="Automatically generate test cases to ensure the correctness of migrate code.",
)
parser.add_argument(
    "-m",
    "--module",
    help="The module to generate tests for. If module ends with a directory, "
         "Versionizer will generate tests for all relevant files in the module. "
         "If module ends with a filename, i.e. some_dir/some_file.py, Versionizer "
         "will only generate tests for that file.",
)
# TODO: user can either generate or run the tests, or both -> but not either
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
parser.set_defaults(generate_tests=True)
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
parser.set_defaults(run_tests=True)
parser.add_argument(
    "-l",
    "--library",
    required=True,
    help="The library being upgraded. Note: this library's name must appear exactly as it does in it's package repository.",
)
parser.add_argument(
    "-p",
    "--previous-version",
    help="The version being upgraded from.",
)
parser.add_argument(
    "-n",
    "--new-version",
    help="The version being upgraded to. If not specified, Versionizer will default to the most recent version available in the package repository.",
)
parser.add_argument(
    "-o",
    "--output-path",
    default="generated_tests",
    help="The path where generated test files will be created.",
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
    if args.generate_tests:
        if not args.module:
            parser.error(
                "If generate-tests flag is set, then you must specify the module or file to generate tests for.")
    if not args.run_tests and not args.generate_tests:
        parser.error(
            "Please specify whether you want Versionizer to generate or run tests.")


def main():
    args = parser.parse_args()
    validate_args(args)
    if args.generate_tests:
        generate_tests(args)
    if args.run_tests:
        run_tests(args)


if __name__ == "__main__":
    main()
