import os
import tempfile

import pytest

from versionizer.ast_differ import ASTDiffer


@pytest.fixture
def temp_file1():
    fd, path = tempfile.mkstemp()
    try:
        func = """
def foo():
    return 1
                    """
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(func)
        yield path
    finally:
        os.remove(path)


@pytest.fixture
def temp_file2():
    fd, path = tempfile.mkstemp()
    try:
        func = """
def foo():
    return 2
                    """
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(func)
        yield path
    finally:
        os.remove(path)


def test_temp_file_fixtures(temp_file1):
    assert os.path.getsize(temp_file1) > 0


def test_get_changed_function_nodes_returns_nothing_for_no_change(temp_file1):
    differ = ASTDiffer(temp_file1, temp_file1)
    assert not differ.get_changed_function_nodes()


def test_get_changed_function_nodes_returns_node_that_was_changed(temp_file1,
                                                                  temp_file2):
    differ = ASTDiffer(temp_file1, temp_file2)
    assert len(differ.get_changed_function_nodes()) == 1
