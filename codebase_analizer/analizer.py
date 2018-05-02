import os
import collections
import shutil

# Python 2/3 compatibility
from builtins import object

from .filters import TokenTypeFilter, PartOfSpeechFilter
from .parsers import TokenNameParser


class CodeBaseAnalizer(object):
    """ Analize collected codebase data """

    def __init__(self, codebase_tokens,
                 target_files_extension='.py',
                 target_token_type='function',
                 target_part_of_speech='VB'):
        self._codebase_tokens = codebase_tokens
        self._filter_token = TokenTypeFilter(target_token_type)
        self._filter_part_of_speech = PartOfSpeechFilter(target_part_of_speech)
        self._token_parser = TokenNameParser(target_files_extension)

    def __str__(self):
        return 'Analize codebase tokens {0}'.format(self._codebase_tokens)

    def _get_codebase_tokens_names(self):
        for token in self._filter_token(self._codebase_tokens):
            yield token.name

    def _get_codebase_words(self, codebase_tokens_names):  # pragma: no cover
        for token_name in codebase_tokens_names:
            parsed_tokens = self._token_parser(token_name)
            for word in self._filter_part_of_speech(parsed_tokens):
                yield word.lower()

    def _get_top_words(self, words, top_size):
        return collections.Counter(words).most_common(top_size)

    def find_top_codebase_words(self, top_size):  # pragma: no cover
        codebase_tokens_names = self._get_codebase_tokens_names()
        codebase_words = self._get_codebase_words(codebase_tokens_names)

        return self._get_top_words(codebase_words, top_size)


class OpenProject(object):
    """
    OpenProject class receives the path of the project
    that should be opened and analized.
    If the project path is an url, repo would be cloned and removed afterall.
    OpenProject is a context manager:
      * Project path
        (whether cloned if project_location is an url
         or one passed to the class)
        is returned during __enter__
      * Project directory is removed during __exit__ if a project was cloned
    """

    def __init__(self, project_location):
        self.clone_repo = self._is_url(project_location)
        self.project_path = self.get_project_path(project_location)

    @staticmethod
    def _is_url(project_location):
        return project_location.startswith('http')

    def _get_project_name(self, project_location):
        project_name = project_location.split('/')[-1]
        if self.clone_repo:
            # Truncate .git postfix
            project_name = project_name.split('.')[0]
        return project_name

    def get_project_path(self, project_location):
        if self.clone_repo:
            # Clone the repo and return project_path
            os.system('git clone {0}'.format(project_location))
            project_name = self._get_project_name(project_location)
            return os.path.join(os.getcwd(), project_name)
        return project_location

    def __enter__(self):
        return self.project_path

    def __exit__(self, exc_type, exc_value, traceback):
        if self.clone_repo:
            shutil.rmtree(self.project_path)
