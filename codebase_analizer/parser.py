import ast
import os

from tqdm import tqdm as progress_bar

# Python 2/3 compatibility
from io import open

from codebase_analizer import filters


def _find_files(path, show_progress, target_files_extension):
    _show_progress = progress_bar if show_progress else lambda x: x
    for dirpath, dirnames, filenames in _show_progress(os.walk(path)):
        for filename in filters.filter_files_by_ext(
            target_files_extension, filenames
        ):
            yield os.path.join(dirpath, filename)


def _open_file(_file):
    with open(_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
    return file_content


def _get_syntax_trees(files):
    for _file in files:
        try:
            file_content = _open_file(_file)
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


def _get_codebase_nodes(files_syntax_trees):  # pragma: no cover
    for tree in files_syntax_trees:
        for node in tree:
            yield node


def get_codebase_tokens(project_path, user_settings):  # pragma: no cover
    codebase_files = _find_files(
        project_path,
        user_settings.show_progress,
        user_settings.files_ext
    )
    codebase_syntax_trees = _get_syntax_trees(codebase_files)

    return _get_codebase_nodes(codebase_syntax_trees)


def parse_token_name(token_name, file_extension):
    """ Parse token name with regard to files extension.
    For instance:
      * python code is written in an undescore case
        so token_names in a python files should be splitted by '_'
    """
    def _get_parse_func(file_extension):
        ext_parser = {'.py': lambda token_name: token_name.split('_'), }
        return ext_parser.get(file_extension, lambda token_name: token_name)

    parse_function = _get_parse_func(file_extension)
    return parse_function(token_name)
