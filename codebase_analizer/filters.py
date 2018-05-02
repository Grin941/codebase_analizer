import ast
import nltk

# Python 2/3 compatibility
from builtins import object

__all__ = ['FilesFilter', 'TokenTypeFilter', 'PartOfSpeechFilter']


class BaseFilter(object):

    def __init__(self, *args, **kwargs):
        self.filter_func = self._get_filter_func(*args, **kwargs)

    def __call__(self, iterable):
        return filter(self.filter_func, iterable)

    def _get_filter_func(self, *args, **kwargs):
        raise NotImplementedError('To be implemented')


class FilesFilter(BaseFilter):

    def __init__(self, file_extension):
        super(FilesFilter, self).__init__(file_extension)

    def __call__(self, filenames):
        return super(FilesFilter, self).__call__(filenames)

    def _get_filter_func(self, file_extension):
        return lambda filename: filename.endswith(file_extension)


class TokenTypeFilter(BaseFilter):

    def __init__(self, token_type):
        super(TokenTypeFilter, self).__init__(token_type)

    def __call__(self, tokens):
        return super(TokenTypeFilter, self).__call__(tokens)

    def _get_filter_func(self, token_type):
        if token_type == 'function':
            return lambda token: isinstance(token, ast.FunctionDef) and not \
                (token.name.startswith('__') and
                 token.name.endswith('__'))
        elif token_type == 'variable':
            return lambda token: isinstance(token, ast.Name)
        else: return lambda token: False


class PartOfSpeechFilter(BaseFilter):

    def __init__(self, part_of_speech):
        super(PartOfSpeechFilter, self).__init__(part_of_speech)

    def __call__(self, words=[]):
        return super(PartOfSpeechFilter, self).__call__(words)

    def _get_filter_func(self, part_of_speech):
        def _is_target_part_of_speech(word=''):
            if not word:
                return False
            pos_info = nltk.pos_tag([word])
            word_tag = pos_info[0][1]
            return word_tag.startswith(part_of_speech)

        return _is_target_part_of_speech
