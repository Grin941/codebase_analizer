import ast
import pytest

from codebase_analizer.analizer import CodeBaseAnalizer

@pytest.fixture(scope="module")
def codebase_tokens_analizer():
    function_token = ast.FunctionDef()
    setattr(function_token, 'name', 'foo_bar')

    class_token = ast.ClassDef()
    setattr(class_token, 'name', 'TestMySelf')

    return CodeBaseAnalizer(
        [function_token, class_token]
    )
