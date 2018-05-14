import ast
import nltk


def apply_filter(filter_factory):
    def filtered_iterable(filter_attr, iterable=[]):
        filter_func = filter_factory(filter_attr, iterable)
        return filter(filter_func, iterable)
    return filtered_iterable


@apply_filter
def filter_files_by_ext(files_ext, filenames):
    """
    Filter filenames
    """
    return lambda filename: filename.endswith(files_ext)


@apply_filter
def filter_token_by_type(token_type, tokens):
    """
    Filter tokens by types (function, variable, etc)
    """
    if token_type == 'function':
        return lambda token: isinstance(token, ast.FunctionDef) and not \
            (token.name.startswith('__') and
             token.name.endswith('__'))
    elif token_type == 'variable':
        return lambda token: isinstance(token, ast.Name)
    else: return lambda token: False


@apply_filter
def filter_words_by_part_of_speech(part_of_speech, words=[]):
    """
    Filter words by part of speech
    (VB, NN, etc)
    """
    def _is_target_part_of_speech(word=''):
        if not word:
            return False
        pos_info = nltk.pos_tag([word])
        word_tag = pos_info[0][1]
        return word_tag.startswith(part_of_speech)

    return _is_target_part_of_speech
