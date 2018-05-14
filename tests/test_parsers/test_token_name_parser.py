from codebase_analizer import codebase_parser


def test_token_name_parser_splits_tokens_by_undescore_for_py_files():
    assert set(codebase_parser.parse_token_name('foo_bar', '.py')) == {'foo', 'bar'}


def test_token_name_parser_returns_token_name_for_not_py_files():
    assert codebase_parser.parse_token_name('foo_bar', '.js') == 'foo_bar'
