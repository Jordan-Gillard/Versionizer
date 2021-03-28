import pytest

from versionizer.cli import parser


@pytest.fixture()
def default_args():
    return ["--library", "fake_lib"]


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


def test_parser_stores_module_with_dir(default_args):
    module = 'some_dir/some_dir/another_dir'
    default_args.extend(['-l', module])
    args = parser.parse_args(default_args)
    assert args.library == module


def test_parser_stores_module_with_file(default_args):
    file = 'some_dir/some_dir/python_file.py'
    default_args.extend(['-l', file])
    args = parser.parse_args(default_args)
    assert args.library == file


def test_parser_stores_library(default_args):
    library = "freezegun"
    args = parser.parse_args(['-l', library])
    assert args.library == library


def test_parser_stores_previous_version(default_args):
    version = "1.0.0"
    default_args.extend(['-p', version])
    args = parser.parse_args(default_args)
    assert args.previous_version == version


def test_parser_stores_new_version(default_args):
    version = "2.0.0"
    default_args.extend(['-n', version])
    args = parser.parse_args(default_args)
    assert args.new_version == version


def test_parser_stores_output_path(default_args):
    path = "some_dir/some_test_dir/"
    default_args.extend(['-o', path])
    args = parser.parse_args(default_args)
    assert args.output_path == path


def test_parser_throws_error_with_bad_algorithm(default_args):
    default_args.extend(["--algorithm", "FAKE_ALGORITHM"])
    with pytest.raises(SystemExit):
        parser.parse_args(default_args)
