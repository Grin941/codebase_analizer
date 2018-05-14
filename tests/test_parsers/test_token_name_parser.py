from codebase_analizer import parser


def test_token_name_parser_splits_tokens_by_undescore_for_py_files():
    assert set(parser.parse_token_name('.py', 'foo_bar')) == {'foo', 'bar'}


def test_token_name_parser_returns_token_name_for_not_py_files():
    assert parser.parse_token_name('.js', 'foo_bar') == 'foo_bar'
