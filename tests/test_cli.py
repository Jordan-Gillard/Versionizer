import io
from contextlib import redirect_stderr

import pytest

from versionizer.cli import parser


@pytest.fixture()
def default_args():
    return ["--previous-commit", "fake_commit_12345", "--project-path", "sample_files/"]


def test_parser_defaults(default_args):
    args = parser.parse_args(default_args)
    assert args.generate_tests
    assert args.run_tests
    assert args.algorithm == "WHOLE_SUITE"


def test_parser_dont_generate_tests(default_args):
    default_args.append('-dgt')
    args = parser.parse_args(default_args)
    assert args.generate_tests is False


def test_parser_dont_run_tests(default_args):
    default_args.append('-dr')
    args = parser.parse_args(default_args)
    assert args.run_tests is False


def test_parser_dont_generate_tests_and_run_tests(default_args):
    default_args.extend(['-dgt', '-r'])
    args = parser.parse_args(default_args)
    assert args.generate_tests is False
    assert args.run_tests


def test_parser_generate_tests_and_dont_run_tests(default_args):
    default_args.extend(['-gt', '-dr'])
    args = parser.parse_args(default_args)
    assert args.generate_tests
    assert args.run_tests is False


def test_parser_throws_error_with_bad_algorithm(default_args):
    default_args.extend(["--algorithm", "FAKE_ALGORITHM"])
    # We don't want the error showing up in the test results
    with redirect_stderr(io.StringIO()):
        with pytest.raises(SystemExit):
            parser.parse_args(default_args)
