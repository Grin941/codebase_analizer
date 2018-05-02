import ast

from codebase_analizer.filters import FilesFilter, TokenTypeFilter, PartOfSpeechFilter


class TestFilesFilter:
    def setup(self):
        self.files_filter = FilesFilter('.py')

    def test_files_filter_returns_files_with_specific_extensions(self):
        files = ('foo.py', 'bar.py', 'tmp.md', 'abrakadabra')

        filtered_files = []
        for _file in self.files_filter(files):
            filtered_files.append(_file)

        assert len(list(
            filter(lambda _file: _file.endswith('.py'), files)
        )) == len(filtered_files)


class TestTokenTypeFilter:

    def setup(self):
        self.function_token = ast.FunctionDef()
        setattr(self.function_token, 'name', 'foo')
        self.magic_function_token = ast.FunctionDef()
        setattr(self.magic_function_token, 'name', '__bar__')
        self.class_token = ast.ClassDef()
        setattr(self.class_token, 'name', 'tmp')
        self.tokens = (self.function_token,
                       self.magic_function_token,
                       self.class_token)

    def test_token_type_filter_returns_not_magic_functions(self):
        token_type_filter = TokenTypeFilter('function')

        filtered_tokens = []
        for token in token_type_filter(self.tokens):
            filtered_tokens.append(token)

        assert len(filtered_tokens) == 1 and \
            filtered_tokens[0] == self.function_token

    def test_token_type_filter_returns_nothing_if_token_type_is_not_function(self):
        token_type_filter = TokenTypeFilter('class')

        filtered_tokens = []
        for token in token_type_filter(self.tokens):
            filtered_tokens.append(token)

        assert not len(filtered_tokens)


class TestPartOfSpeechFilter:
    def setup(self):
        self.part_of_speech_filter = PartOfSpeechFilter('VB')

    def test_whether_word_is_verb(self):
        nltk_tags = {
            'VB': 'go',
            'VBG': 'focusing',
            'VBN': 'desired',
            'NN': 'Fulton',
            'AT': 'The',
        }

        for tag, word in nltk_tags.items():
            if tag.startswith('VB'):
                assert len(list(self.part_of_speech_filter([word])))
            else:
                assert not len(list(self.part_of_speech_filter([word])))

    def test_is_verb_returns_false_if_no_word_was_passed(self):
        assert not len(list(self.part_of_speech_filter()))
