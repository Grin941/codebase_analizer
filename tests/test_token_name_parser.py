from codebase_analizer.parsers import TokenNameParser


def test_token_name_parser_splits_tokens_by_undescore_for_py_files():
    token_name_parser = TokenNameParser('.py')

    assert set(token_name_parser('foo_bar')) == {'foo', 'bar'}


def test_token_name_parser_returns_token_name_for_not_py_files():
    token_name_parser = TokenNameParser('.js')

    assert token_name_parser('foo_bar') == 'foo_bar'
