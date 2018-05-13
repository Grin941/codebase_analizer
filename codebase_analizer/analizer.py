import collections

from .filters import TokenTypeFilter, PartOfSpeechFilter
from .parsers import TokenNameParser


def _get_codebase_tokens_names(
    codebase_tokens, **user_settings
):
    _filter_token = TokenTypeFilter(
        user_settings.get('target_token_type', 'function')
    )

    for token in _filter_token(codebase_tokens):
        yield token.name


def _get_codebase_words(
    codebase_tokens_names, **user_settings
):  # pragma: no cover
    _filter_part_of_speech = PartOfSpeechFilter(
        user_settings.get('target_part_of_speech', '')
    )
    _token_parser = TokenNameParser(
        user_settings.get('target_files_extension', '.py')
    )

    for token_name in codebase_tokens_names:
        parsed_tokens = _token_parser(token_name)
        for word in _filter_part_of_speech(parsed_tokens):
            yield word.lower()


def _get_top_words(words, top_size):
    return collections.Counter(words).most_common(top_size)


def find_top_codebase_words(
    codebase_tokens, top_size, **user_settings
):  # pragma: no cover
    codebase_tokens_names = _get_codebase_tokens_names(
        codebase_tokens, user_settings
    )
    codebase_words = _get_codebase_words(codebase_tokens_names, user_settings)

    return _get_top_words(codebase_words, top_size)
