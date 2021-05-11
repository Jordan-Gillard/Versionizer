import pytest

from tests.shared_functions import generate_temp_file_with_content
from versionizer.ast_handler import ASTHandler


@pytest.fixture
def file_with_indirect_function_dependencies():
    funcs = """def foo():\n    x = 1\n    return bar(x)\n
def bar(a):\n    return a + baz()\n
def baz():\n    return 5"""
    for file in generate_temp_file_with_content(funcs):
        yield file


def test_ast_handler_get_all_function_nodes(file_with_indirect_function_dependencies):
    handler = ASTHandler(file_with_indirect_function_dependencies)
    nodes = handler.get_function_nodes()
    assert len(nodes) == 3


def test_ast_handler_get_functions_dependents(file_with_indirect_function_dependencies):
    handler = ASTHandler(file_with_indirect_function_dependencies)
    dependents = handler.get_function_dependents()
    assert dependents['bar'] == {'foo'}
    assert dependents['baz'] == {'bar'}
    assert 'foo' not in dependents.keys()  # No function calls foo
