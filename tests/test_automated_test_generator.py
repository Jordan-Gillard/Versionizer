import io
import ntpath
import os
import pathlib
import tempfile
from contextlib import redirect_stdout

import pytest

from tests.shared_functions import generate_temp_file_with_content
from versionizer.automated_test_generator import AutomatedTestGenerator


@pytest.fixture
def atg():
    return AutomatedTestGenerator("")


def test_clean_filename(atg):
    dirty_filename = "some_dir/some_file.py"
    clean_filename = "some_dir/some_file"
    assert atg._clean_filename(dirty_filename) == clean_filename


def test_is_file_with_good_file(atg):
    this_file = os.path.abspath(__file__)
    assert atg._is_file(this_file)


def test_is_file_with_bad_file(atg):
    bad_file = "IAmABadFile.py"
    assert not atg._is_file(bad_file)


def test_is_file_with_dir(atg):
    parent_dir = pathlib.Path(__file__).parent
    assert atg._is_file(parent_dir) is False


def test_get_test_files_in_dir(atg):
    parent_dir = pathlib.Path(__file__).parent
    atg_files = atg._get_test_files_in_dir(parent_dir)
    os_files = os.listdir(parent_dir)
    assert len(atg_files) == len([f for f in os_files if "test" in f])


def test_generate_tests_with_file(atg):
    # Capture STDOUT from Pynguin so it doesn't clog up test results
    with redirect_stdout(io.StringIO()):
        # TODO: PyTest comes with built in temporary directory fixtures. Use those.
        with tempfile.TemporaryDirectory() as temp_dir:
            func = "def foo():\n    return 1\n"
            for temp_file_full_path in generate_temp_file_with_content(func):
                project_path = str(pathlib.Path(temp_file_full_path).parent) + \
                               os.path.sep
                atg.project_path = project_path
                atg.output_path = temp_dir
                _, filename = ntpath.split(temp_file_full_path)
                atg.module = filename
                atg.generate_tests()
                files_after = os.listdir(temp_dir)
                assert len(files_after) == 2


def test_generate_tests_with_dir(atg):
    """Tests That Pynguin generates tests for all Python files in a directory."""
    # Capture STDOUT from Pynguin so it doesn't clog up test results
    with redirect_stdout(io.StringIO()):
        # TODO: PyTest comes with built in temporary directory fixtures. Use those.
        with tempfile.TemporaryDirectory() as temp_dir:
            func1 = "def foo():\n    return 1\n"
            for filepath1 in generate_temp_file_with_content(func1):
                func2 = "def foo():\n    return 1\n"
                for filepath2 in generate_temp_file_with_content(func2):
                    project_path = str(pathlib.Path(filepath2).parent) + \
                                   os.path.sep
                    atg.project_path = project_path
                    atg.output_path = temp_dir
                    atg.module = ""
                    atg.generate_tests()
                    files_after = os.listdir(temp_dir)
                    assert len(files_after) == 4


def test_generate_tests_with_dir_recursively():
    """Tests That Pynguin generates tests for all Python files in a directory,
    and all files in subdirectories as well."""
    pass
