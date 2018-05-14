from codebase_analizer import analizer


def test_get_codebase_token_names_returns_token_names(
        codebase_tokens, monkeypatch
):
    def monkey_token_filter(token_names):
        return filter(lambda token_name: True, token_names)
    monkeypatch.setattr(
        analizer._get_codebase_tokens_names,
        '_filter_token',
        monkey_token_filter
    )

    assert set(analizer._get_codebase_tokens_names(codebase_tokens)) == \
        {'foo_bar', 'TestMySelf'}


def test_get_top_words():
    assert set(
        analizer._get_top_words(
            ['one', 'two', 'two', 'three', 'three', 'three'], 10
        )
    ) == {('one', 1), ('two', 2), ('three', 3)}
