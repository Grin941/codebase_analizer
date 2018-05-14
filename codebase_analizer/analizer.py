import collections

from codebase_analizer import filters, parser


def _get_codebase_tokens_names(
    codebase_tokens, target_token_type
):
    for token in filters.filter_token_by_type(
        target_token_type, codebase_tokens
    ):
        yield token.name


def _get_codebase_words(
    codebase_tokens_names, target_part_of_speech, target_files_extension
):  # pragma: no cover
    for token_name in codebase_tokens_names:
        parsed_tokens = parser.parse_token_name(
            token_name, target_files_extension
        )
        for word in filters.filter_words_by_part_of_speech(
            target_part_of_speech, parsed_tokens
        ):
            yield word.lower()


def _get_top_words(words, top_size):
    return collections.Counter(words).most_common(top_size)


def find_top_codebase_words(
    codebase_tokens, user_settings
):  # pragma: no cover
    top_size = user_settings.top_size
    codebase_tokens_names = _get_codebase_tokens_names(
        codebase_tokens, user_settings.token_type
    )
    codebase_words = _get_codebase_words(
        codebase_tokens_names,
        user_settings.part_of_speech,
        user_settings.files_ext
    )

    return _get_top_words(codebase_words, top_size)
