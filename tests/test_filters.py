import ast
import pytest
import collections

from codebase_analizer.filters import \
    FilesFilter, TokenTypeFilter, PartOfSpeechFilter


@pytest.fixture
def files_filter():
    return FilesFilter('.py')


@pytest.fixture
def token_types():
    function_token = ast.FunctionDef()
    setattr(function_token, 'name', 'foo')
    magic_function_token = ast.FunctionDef()
    setattr(magic_function_token, 'name', '__bar__')
    class_token = ast.ClassDef()
    setattr(class_token, 'name', 'tmp')

    Tokens = collections.namedtuple(
        'Tokens', ['function_token', 'magic_function_token', 'class_token']
    )

    return Tokens(
        function_token,
        magic_function_token,
        class_token
    )


@pytest.fixture
def part_of_speech_filter():
    return PartOfSpeechFilter('VB')


def test_files_filter_returns_files_with_specific_extensions(files_filter):
    files = ('foo.py', 'bar.py', 'tmp.md', 'abrakadabra')

    filtered_files = []
    for _file in files_filter(files):
        filtered_files.append(_file)

    assert len(list(
        filter(lambda _file: _file.endswith('.py'), files)
    )) == len(filtered_files)


def test_token_type_filter_returns_not_magic_functions(token_types):
    token_type_filter = TokenTypeFilter('function')

    filtered_tokens = []
    for token in token_type_filter(token_types):
        filtered_tokens.append(token)

    assert len(filtered_tokens) == 1 and \
        filtered_tokens[0] == token_types.function_token


def test_token_type_filter_returns_nothing_if_token_type_is_not_function(
    token_types
):
    token_type_filter = TokenTypeFilter('class')

    filtered_tokens = []
    for token in token_type_filter(token_types):
        filtered_tokens.append(token)

    assert not len(filtered_tokens)


def test_whether_word_is_verb(part_of_speech_filter):
    nltk_tags = {
        'VB': 'go',
        'VBG': 'focusing',
        'VBN': 'desired',
        'NN': 'Fulton',
        'AT': 'The',
    }

    for tag, word in nltk_tags.items():
        if tag.startswith('VB'):
            assert len(list(part_of_speech_filter([word])))
        else:
            assert not len(list(part_of_speech_filter([word])))


def test_is_verb_returns_false_if_no_word_was_passed(
    part_of_speech_filter
):
    assert not len(list(part_of_speech_filter()))
