import pytest

from versionizer.cli import parser


def test_parser_defaults():
    args = parser.parse_args([])
    assert args.generate_tests
    assert args.run_tests
    assert args.algorithm == "WHOLE_SUITE"


def test_parser_dont_generate_tests():
    args = parser.parse_args(['-dgt'])
    assert args.generate_tests is False


def test_parser_dont_run_tests():
    args = parser.parse_args(['-dr'])
    assert args.run_tests is False


def test_parser_dont_generate_tests_and_run_tests():
    args = parser.parse_args(['-dgt', '-r'])
    assert args.generate_tests is False
    assert args.run_tests


def test_parser_generate_tests_and_dont_run_tests():
    args = parser.parse_args(['-gt', '-dr'])
    assert args.generate_tests
    assert args.run_tests is False


def test_parser_stores_module_with_dir():
    module = 'some_dir/some_dir/another_dir'
    args = parser.parse_args(['-l', module])
    assert args.library == module


def test_parser_stores_module_with_file():
    file = 'some_dir/some_dir/python_file.py'
    args = parser.parse_args(['-l', file])
    assert args.library == file


def test_parser_stores_library():
    library = "freezegun"
    args = parser.parse_args(['-l', library])
    assert args.library == library


def test_parser_stores_previous_version():
    version = "1.0.0"
    args = parser.parse_args(['-p', version])
    assert args.previous_version == version


def test_parser_stores_new_version():
    version = "2.0.0"
    args = parser.parse_args(['-n', version])
    assert args.new_version == version


def test_parser_stores_output_path():
    path = "some_dir/some_test_dir/"
    args = parser.parse_args(['-o', path])
    assert args.output_path == path


def test_parser_throws_error_with_bad_algorithm():
    with pytest.raises(SystemExit):
        parser.parse_args(["--algorithm", "FAKE_ALGORITHM"])
