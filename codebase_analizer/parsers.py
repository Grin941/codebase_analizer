import ast
import os

from tqdm import tqdm as progress_bar

# Python 2/3 compatibility
from io import open
from builtins import object

from .filters import FilesFilter


class CodeBaseParser(object):
    """ Traverse and parse codebase """

    def __init__(self, path, file_extension='.py', show_progress=False):
        self._path = path
        self._show_progress = progress_bar if show_progress else lambda x: x
        self._filter_files = FilesFilter(file_extension)

    def __str__(self):
        return 'Parse codebase from {0}'.format(self._path)

    def _find_files(self):
        for dirpath, dirnames, filenames in \
                self._show_progress(os.walk(self._path)):
            for filename in self._filter_files(filenames):
                yield os.path.join(dirpath, filename)

    @staticmethod
    def _open_file(_file):
        with open(_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        return file_content

    def _get_syntax_trees(self, files):
        for _file in files:
            try:
                file_content = self._open_file(_file)
                parsed_file_content = ast.parse(file_content)
                yield ast.walk(parsed_file_content)
            except (SyntaxError, ValueError, OSError):
                """
                Errors examples:
                SyntaxError     -       except IOError, err:
                ValueError      -       file_content contains null bytes
                OSError         -       file does not exist
                """
                pass

    def _get_codebase_nodes(self, files_syntax_trees):  # pragma: no cover
        for tree in files_syntax_trees:
            for node in tree:
                yield node

    def get_codebase_tokens(self):  # pragma: no cover
        codebase_files = self._find_files()
        codebase_syntax_trees = self._get_syntax_trees(codebase_files)

        return self._get_codebase_nodes(codebase_syntax_trees)


class TokenNameParser(object):
    """ Parse token name with regard to files extension.
    For instase:
      * python code is written in an undescore case
        so token_names in a python files should be splitted by '_'
    """

    def __init__(self, file_extension):
        self._parse_func = self._get_parse_func(file_extension)

    def __call__(self, token_name):
        return self._parse_func(token_name)

    def _get_parse_func(self, file_extension):
        ext_parser = {'.py': lambda token_name: token_name.split('_'), }
        return ext_parser.get(file_extension, lambda token_name: token_name)
