#!/usr/bin/env python3
import argparse

from automated_test_generator import AutomatedTestGenerator

parser = argparse.ArgumentParser(
    description="Automatically generate test cases to ensure the correctness of migrate code.",
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "-m",
    "--module",
    help="The module to generate tests for. Versionizer will generate tests for all relevant files in the module.",
)
group.add_argument(
    "-f",
    "--file",
    help="The file to generate tests for. Versionizer will generate tests for all relevant functions in the file.",
)
parser.add_argument(
    "-l",
    "--library",
    # required=True,
    help="The library being upgraded. Note: this library's name must appear exactly as it does in it's package repository.",
)
parser.add_argument(
    "-p",
    "--previous-version",
    # required=True,
    help="The version being upgraded from.",
)
parser.add_argument(
    "-n",
    "--new-version",
    # required=True,
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
    default="RANDOM",
    help="Specify which algorithm to use for test generation.",
    choices=["RANDOM", "MOSA", "RANDOM_SEARCH", "WHOLE_SUITE"],
)


if __name__ == "__main__":
    args = parser.parse_args()
    test_generator = AutomatedTestGenerator(args)
    test_generator.generate_tests()
