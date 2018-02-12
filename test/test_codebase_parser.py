import os
import pytest

from parsers import CodeBaseParser


class TestCodebaseParser:
    def setup(self):
        self.codebase_analizer = CodeBaseParser('')

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

        def monkey_files_filter(_file):
            return lambda x: True
        monkeypatch.setattr(self.codebase_analizer, '_filter_files',
                            monkey_files_filter)

        files = self.codebase_analizer._find_files()
        assert {'/foo/baz', '/foo/bar/spam', '/foo/bar/eggs'} == set(files)

    def test_filenames_finder_finds_specific_files(self, monkeypatch):
        def monkey_os_walk(path):
            return [
                ('/foo', ('bar',), ('baz.py',)),
                ('/foo/bar', (), ('123.py', 'eggs.js')),
            ]
        monkeypatch.setattr(os, "walk", monkey_os_walk)
        assert set(self.codebase_analizer._find_files()) == \
            {'/foo/baz.py', '/foo/bar/123.py'}

    def test_get_syntax_tree_method_dont_fail_if_file_not_exist(self):
        files = ('/foo.baz.py', )
        try:
            self.codebase_analizer._get_syntax_trees(files)
        except Exception as exc:
            pytest.fail('{} was raised'.format(exc))
