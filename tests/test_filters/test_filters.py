from codebase_analizer import filters


def test_files_filter_returns_files_with_specific_extensions():
    files = ('foo.py', 'bar.py', 'tmp.md', 'abrakadabra')

    filtered_files = []
    for _file in filters.filter_files_by_ext('.py', files):
        filtered_files.append(_file)

    assert len(list(
        filter(lambda _file: _file.endswith('.py'), files)
    )) == len(filtered_files)


def test_token_type_filter_returns_not_magic_functions(token_types):
    filtered_tokens = []
    for token in filters.filter_token_by_type('function', token_types):
        filtered_tokens.append(token)

    assert len(filtered_tokens) == 1 and \
        filtered_tokens[0] == token_types.function_token


def test_token_type_filter_returns_nothing_if_token_type_is_not_function(
    token_types
):
    filtered_tokens = []
    for token in filters.filter_token_by_type('class', token_types):
        filtered_tokens.append(token)

    assert not len(filtered_tokens)


def test_whether_word_is_verb():
    nltk_tags = {
        'VB': 'go',
        'VBG': 'focusing',
        'VBN': 'desired',
        'NN': 'Fulton',
        'AT': 'The',
    }

    for tag, word in nltk_tags.items():
        if tag.startswith('VB'):
            assert len(list(filters.filter_words_by_part_of_speech('VB', [word])))
        else:
            assert not len(list(filters.filter_words_by_part_of_speech('VB', [word])))


def test_is_verb_returns_false_if_no_word_was_passed():
    assert not len(list(filters.filter_words_by_part_of_speech('VB')))
