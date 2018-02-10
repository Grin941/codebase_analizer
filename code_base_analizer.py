import ast
import os
import collections
import argparse
import shutil

from tqdm import tqdm as progress_bar

# Python 2/3 compatibility
from io import open
from builtins import object

from filters import FilesFilter, TokenTypeFilter, PartOfSpeechFilter
from report_generators import StdoutReportGenerator, \
    CsvReportGenerator, JsonReportGenerator


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
            for filename in filter(self._filter_files, filenames):
                yield os.path.join(dirpath, filename)

    def _get_syntax_trees(self, files):
        for _file in files:
            try:
                file_content = open(_file, 'r', encoding='utf-8').read()
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
        for token in filter(self._filter_token, self._codebase_tokens):
            yield token.name

    def _get_codebase_words(self, codebase_tokens_names):  # pragma: no cover
        for token_name in codebase_tokens_names:
            for word in filter(self._filter_part_of_speech,
                               self._token_parser(token_name)):
                yield word.lower()

    def _get_top_words(self, words, top_size):
        return collections.Counter(words).most_common(top_size)

    def find_top_codebase_words(self, top_size):  # pragma: no cover
        codebase_tokens_names = self._get_codebase_tokens_names()
        codebase_words = self._get_codebase_words(codebase_tokens_names)

        return self._get_top_words(codebase_words, top_size)


class ReportDataGenerator(object):
    """ Generates data for a code base report """

    def __init__(self, popular_words):
        """
        :param popular_words: collections.Counter object
        """
        self._popular_words = popular_words

    def generate_report_data(self):
        total_words_count = sum(word_occurance for
                                word, word_occurance in self._popular_words)
        unique_words_count = len(self._popular_words)

        return total_words_count, unique_words_count, self._popular_words


class CodeBaseReportService(object):  # pragma: no cover
    """ Display code base report """

    report_generator_factory = {
        'stdout': StdoutReportGenerator,
        'csv': CsvReportGenerator,
        'json': JsonReportGenerator,
    }

    def __init__(self, report_data, report_format):
        self._report_data = report_data
        self._report_generator = \
            self.report_generator_factory.get(
                report_format, StdoutReportGenerator)(report_format)

    def show_top_words_report(self):
        self._report_generator.generate_report(self._report_data)


class OpenProject(object):

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find most popular words in your codebase.')
    parser.add_argument('project_location', type=str,
                        help="""root path of your project or
                                url to clone the repo from""")
    parser.add_argument('--files-ext', default='.py', const='.py',
                        nargs='?', choices=['.py', ],
                        help="""files extension you want to analize
                                (default: %(default)s)""")
    parser.add_argument('--token-type', default='function', const='function',
                        nargs='?', choices=['function', 'variable'],
                        help="""what token type do you want to analize:
                                function or variable
                                (default: %(default)s)?""")
    parser.add_argument('--part-of-speech', default='VB', const='VB',
                        nargs='?', choices=['VB', 'NN'],
                        help="""what type of speech do you want to analize:
                                verb or noun
                                (default: %(default)s)?""")
    parser.add_argument('--report-format', default='stdout', const='stdout',
                        nargs='?', choices=['stdout', 'csv', 'json'],
                        help="""how do you want to see your report:
                                print to stdout or generate json/scv file
                                (default: %(default)s)?""")
    parser.add_argument('--top-size', type=int, default=10,
                        help="""how long top list would you like to see
                                (default: %(default)s)?""")
    parser.add_argument('--show-progress', action='store_true',
                        help='do you want to see progress bar?')
    args = parser.parse_args()

    with OpenProject(args.project_location) as project_path:
        codebase_parser = CodeBaseParser(project_path, args.files_ext,
                                         args.show_progress)
        codebase_tokens = codebase_parser.get_codebase_tokens()

        codebase_analizer = CodeBaseAnalizer(codebase_tokens, args.files_ext,
                                             args.token_type,
                                             args.part_of_speech)
        popular_words = codebase_analizer.find_top_codebase_words(
            args.top_size)

        report_data_generator = ReportDataGenerator(popular_words)
        report_data = report_data_generator.generate_report_data()

        codebase_reporter = CodeBaseReportService(report_data,
                                                  args.report_format)
        codebase_reporter.show_top_words_report()
