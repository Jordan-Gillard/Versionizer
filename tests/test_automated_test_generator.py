import os
import pathlib
from argparse import Namespace

import pytest

from versionizer.automated_test_generator import AutomatedTestGenerator


@pytest.fixture
def atg():
    return AutomatedTestGenerator(Namespace())


def test_clean_filename(atg):
    dirty_filename = "some_dir/some_file.py"
    clean_filename = "some_dir/some_file"
    assert atg._clean_filename(dirty_filename) == clean_filename


def test_is_file_with_file(atg):
    this_file = os.path.abspath(__file__)
    assert atg._is_file(this_file)


def test_is_file_with_dir(atg):
    parent_dir = pathlib.Path(__file__).parent
    assert atg._is_file(parent_dir) is False


def test_clean_path(atg):
    dirty_path = os.path.join("some_dir", "another_dir", "file.py")
    clean_path = "some_dir.another_dir.file.py"
    assert atg._clean_path(dirty_path) == clean_path
