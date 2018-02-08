import os
import pytest

from code_base_analizer import CodeBaseParser


class TestCodebaseParser:
    def setup(self):
        self.codebase_analizer = CodeBaseParser('')

    def test_files_finder_dont_fail_on_unexisting_path(self):
        files_gen = self.codebase_analizer._find_files()
        assert not len(list(files_gen))

    #def test_files_finder_returns_full_path(self, monkeypatch):
    #    def monkey_os_walk(path):
    #        return [
    #            ('/foo', ('bar',), ('baz',)),
    #            ('/foo/bar', (), ('spam', 'eggs')),
    #        ]
    #    monkeypatch.setattr(os, "walk", monkey_os_walk)

    #    files = self.codebase_analizer._find_files()
    #    assert {'/foo/baz', '/foo/bar/spam', '/foo/bar/eggs'} == set(files)

    #def test_files_filter_is_filterinf_files_by_an_extension(self):
    #    files = ('/foo/baz.py', '/foo/bar/readmi.md', '/foo/123.py', '123123')

    #    assert set(self.codebase_analizer._filter_files(files)) == \
    #        {'/foo/baz.py', '/foo/123.py'}

    #def test_get_syntax_tree_method_dont_fail_if_file_not_exist(self):
    #    files = ('/foo.baz.py', )
    #    try:
    #        self.codebase_analizer._get_syntax_trees(files)
    #    except Exception as exc:
    #        pytest.fail('{} was raised'.format(exc))
