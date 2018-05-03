import ast
import pytest

from codebase_analizer.analizer import CodeBaseAnalizer


@pytest.fixture
def codebase_tokens_analizer():
    function_token = ast.FunctionDef()
    setattr(function_token, 'name', 'foo_bar')

    class_token = ast.ClassDef()
    setattr(class_token, 'name', 'TestMySelf')

    return CodeBaseAnalizer(
        [function_token, class_token]
    )


def test_get_codebase_token_names_returns_token_names(
        codebase_tokens_analizer, monkeypatch
):
    def monkey_token_filter(token_names):
        return filter(lambda token_name: True, token_names)
    monkeypatch.setattr(codebase_tokens_analizer, '_filter_token',
                        monkey_token_filter)

    assert set(codebase_tokens_analizer._get_codebase_tokens_names()) == \
        {'foo_bar', 'TestMySelf'}


def test_get_top_words(codebase_tokens_analizer):
    assert set(
        codebase_tokens_analizer._get_top_words(
            ['one', 'two', 'two', 'three', 'three', 'three'], 10
        )
    ) == {('one', 1), ('two', 2), ('three', 3)}
