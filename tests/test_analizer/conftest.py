import ast
import pytest


@pytest.fixture(scope="module")
def codebase_tokens():
    function_token = ast.FunctionDef()
    setattr(function_token, 'name', 'foo_bar')

    class_token = ast.ClassDef()
    setattr(class_token, 'name', 'TestMySelf')

    return [function_token, class_token]
