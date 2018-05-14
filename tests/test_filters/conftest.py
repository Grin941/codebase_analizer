import ast
import pytest
import collections


@pytest.fixture(scope='module')
def token_types():
    function_token = ast.FunctionDef()
    setattr(function_token, 'name', 'foo')
    magic_function_token = ast.FunctionDef()
    setattr(magic_function_token, 'name', '__bar__')
    class_token = ast.ClassDef()
    setattr(class_token, 'name', 'tmp')

    tokens = collections.namedtuple(
        'tokens', ['function_token', 'magic_function_token', 'class_token']
    )

    return tokens(
        function_token,
        magic_function_token,
        class_token
    )
