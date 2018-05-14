import os
from codebase_analizer import codebase_parser, filters


def test_files_finder_dont_fail_on_unexisting_path():
    files_gen = codebase_parser._find_files('', True, '.py')
    assert not len(list(files_gen))


def test_files_finder_returns_full_path(monkeypatch):
    def monkey_os_walk(path):
        return [
            ('/foo', ('bar',), ('baz',)),
            ('/foo/bar', (), ('spam', 'eggs')),
        ]
    monkeypatch.setattr(os, "walk", monkey_os_walk)

    def monkey_files_filter(files_ext, _files):
        return filter(lambda x: True, _files)
    monkeypatch.setattr(filters, 'filter_files_by_ext',
                        monkey_files_filter)

    files = codebase_parser._find_files('', True, '.py')
    assert {'/foo/baz', '/foo/bar/spam', '/foo/bar/eggs'} == set(files)


def test_filenames_finder_finds_specific_files(monkeypatch):
    def monkey_os_walk(path):
        return [
            ('/foo', ('bar',), ('baz.py',)),
            ('/foo/bar', (), ('123.py', 'eggs.js')),
        ]
    monkeypatch.setattr(os, "walk", monkey_os_walk)
    assert set(codebase_parser._find_files('', True, '.py')) == \
        {'/foo/baz.py', '/foo/bar/123.py'}


def test_get_syntax_tree_method_dont_fail_if_file_not_exist():
    files = ('/foo.baz.py', )
    try:
        codebase_parser._get_syntax_trees(files)
    except Exception as exc:
        pytest.fail('{} was raised'.format(exc))
