import os
from codebase_analizer import parser as codebase_parser


def test_files_finder_dont_fail_on_unexisting_path(codebase_parser):
    files_gen = codebase_parser._find_files()
    assert not len(list(files_gen))


def test_files_finder_returns_full_path(codebase_parser, monkeypatch):
    def monkey_os_walk(path):
        return [
            ('/foo', ('bar',), ('baz',)),
            ('/foo/bar', (), ('spam', 'eggs')),
        ]
    monkeypatch.setattr(os, "walk", monkey_os_walk)

    def monkey_files_filter(_files):
        return filter(lambda x: True, _files)
    monkeypatch.setattr(codebase_parser, '_filter_files',
                        monkey_files_filter)

    files = codebase_parser._find_files()
    assert {'/foo/baz', '/foo/bar/spam', '/foo/bar/eggs'} == set(files)


def test_filenames_finder_finds_specific_files(codebase_parser, monkeypatch):
    def monkey_os_walk(path):
        return [
            ('/foo', ('bar',), ('baz.py',)),
            ('/foo/bar', (), ('123.py', 'eggs.js')),
        ]
    monkeypatch.setattr(os, "walk", monkey_os_walk)
    assert set(codebase_parser._find_files()) == \
        {'/foo/baz.py', '/foo/bar/123.py'}


def test_get_syntax_tree_method_dont_fail_if_file_not_exist(codebase_parser):
    files = ('/foo.baz.py', )
    try:
        codebase_parser._get_syntax_trees(files)
    except Exception as exc:
        pytest.fail('{} was raised'.format(exc))
