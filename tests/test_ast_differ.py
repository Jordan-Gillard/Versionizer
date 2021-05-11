import os
import tempfile

import pytest

from versionizer.ast_differ import ASTDiffer
from versionizer.ast_handler import ASTHandler


def generate_temp_file_with_content(content):
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(str.encode(content))
    tmp.seek(0)
    yield tmp.name
    tmp.close()


@pytest.fixture
def temp_file1():
    func = """def foo():\n    return 1"""
    for filename in generate_temp_file_with_content(func):
        yield filename


@pytest.fixture
def temp_file2():
    func = """def foo():\n    return 2"""
    for filename in generate_temp_file_with_content(func):
        yield filename


def test_temp_file_fixtures(temp_file1):
    assert os.path.getsize(temp_file1) > 0


def test_get_changed_function_nodes_returns_nothing_for_no_change(temp_file1):
    handler1 = ASTHandler(temp_file1)
    handler2 = ASTHandler(temp_file1)
    differ = ASTDiffer(handler1, handler2)
    assert not differ.get_changed_function_nodes()


def test_get_changed_function_nodes_returns_node_that_was_changed(temp_file1,
                                                                  temp_file2):
    handler1 = ASTHandler(temp_file1)
    handler2 = ASTHandler(temp_file2)
    differ = ASTDiffer(handler1, handler2)
    assert len(differ.get_changed_function_nodes()) == 1
