from tests.shared_functions import generate_temp_file_with_content
from versionizer.ast_differ import ASTDiffer
from versionizer.ast_handler import ASTHandler
from versionizer.parsed_ast_builder import ParsedASTBuilder


# TODO: Clean up this test file. Theres too much duplicate code.

def test_build_source_with_one_simple_function():
    func = "def foo():\n    return\n"
    for full_path_tempfile in generate_temp_file_with_content(func):
        handler = ASTHandler(full_path_tempfile)
        func_nodes = {n for n in handler.get_function_nodes().keys()}
        deps = handler.get_function_dependents()
        builder = ParsedASTBuilder(full_path_tempfile, func_nodes, deps)
        builder.build_source()
        with open(full_path_tempfile, 'r') as f:
            assert f.read() == func


def test_build_source_with_two_funcs_but_only_one_changed():
    """
    Asserts that the rewritten file only has the one function that changed. In this
    test, the changed function is `bar()` which goes from returning None to returning
    1. The function in the rewritten file should be the original form of the function
    before the change, i.e. bar() -> None.
    """
    func1 = "def foo():\n    return\n"
    func2 = "def bar():\n    return\n"
    for full_path_tempfile_1 in generate_temp_file_with_content(func1+func2):
        func3 = "def bar():\n    return 1\n"
        for full_path_tempfile_2 in generate_temp_file_with_content(func1 + func3):
            handler_1 = ASTHandler(full_path_tempfile_1)
            handler_2 = ASTHandler(full_path_tempfile_2)
            differ = ASTDiffer(handler_1, handler_2)
            func_nodes = differ.get_changed_function_nodes()
            deps = handler_1.get_function_dependents()
            builder = ParsedASTBuilder(full_path_tempfile_1, func_nodes, deps)
            builder.build_source()
            with open(full_path_tempfile_1, 'r') as f:
                assert f.read() == func2


def test_build_source_which_includes_indirectly_dependent_funcs():
    func1 = "def foo():\n    return bar()\n"
    func2 = "def bar():\n    return baz()\n"
    func3 = "def baz():\n    return 1\n"
    for full_path_tempfile_1 in generate_temp_file_with_content(func1+func2+func3):
        func4 = "def foo():\n    return bar() + 1\n"
        for full_path_tempfile_2 in generate_temp_file_with_content(func4+func2+func3):
            handler_1 = ASTHandler(full_path_tempfile_1)
            handler_2 = ASTHandler(full_path_tempfile_2)
            differ = ASTDiffer(handler_1, handler_2)
            func_nodes = differ.get_changed_function_nodes()
            deps = handler_1.get_function_dependents()
            builder = ParsedASTBuilder(full_path_tempfile_1, func_nodes, deps)
            builder.build_source()
            with open(full_path_tempfile_1, 'r') as f:
                content = f.read()
                assert content.replace("\n", "") == (func1+func2+func3).replace("\n", "")
