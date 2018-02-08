import pytest
import ast

from filters import FilesFilter, TokenTypeFilter, PartOfSpeechFilter


class TestFilesFilter:
    def setup(self):
        self.files_filter = FilesFilter('.py')

    def test_files_filter_returns_files_with_specific_extensions(self):
        files = ('foo.py', 'bar.py', 'tmp.md', 'abrakadabra')

        filtered_files = []
        for _file in files:
            if self.files_filter(_file):
                filtered_files.append(_file)

        assert len(list(
            filter(lambda _file: _file.endswith('.py'), files)
        )) == len(filtered_files)


class TestTokenTypeFilter:

    def setup(self):
        self.function_token = ast.FunctionDef('foo', '', '', '', '')
        self.magic_function_token = ast.FunctionDef('__bar__', '', '', '', '')
        self.class_token = ast.ClassDef('tmp', '', '', '', '')

        self.tokens = (self.function_token,
                       self.magic_function_token,
                       self.class_token)

    def test_token_type_filter_returns_not_magic_functions(self):
        token_type_filter = TokenTypeFilter('function')

        filtered_tokens = []
        for token in self.tokens:
            if token_type_filter(token):
                filtered_tokens.append(token)

        assert len(filtered_tokens) == 1 and \
            filtered_tokens[0] == self.function_token

    def test_token_type_filter_returns_nothing_if_token_type_is_not_function(self):
        token_type_filter = TokenTypeFilter('class')

        filtered_tokens = []
        for token in self.tokens:
            if token_type_filter(token):
                filtered_tokens.append(token)

        assert not len(filtered_tokens)
