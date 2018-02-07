import os

from code_base_analizer import CodeBaseAnalizer


class TestCodebaseAnalizer:
    def setup(self):
        self.codebase_analizer = CodeBaseAnalizer('')

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
                assert self.codebase_analizer._is_verb(word)
            else:
                assert not self.codebase_analizer._is_verb(word)

    def test_files_finder_dont_fail_on_unexisting_path(self):
        files_gen = self.codebase_analizer._find_files()
        assert not len(list(files_gen))

    def test_files_finder_returns_full_path(self, monkeypatch):
        def monkey_os_walk(path):
            return [
                ('/foo', ('bar',), ('baz',)),
                ('/foo/bar', (), ('spam', 'eggs')),
            ]
        monkeypatch.setattr(os, "walk", monkey_os_walk)

        files = self.codebase_analizer._find_files()
        assert {'/foo/baz', '/foo/bar/spam', '/foo/bar/eggs'} == set(files)
