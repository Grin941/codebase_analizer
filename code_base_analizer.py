import ast
import os
import collections
import nltk
import argparse

from tqdm import tqdm as progress_bar

# Python 2/3 compatibility
from io import open
from builtins import object


class FilesFilter(object):

    def __init__(self, file_extension):
        self.filter_func = self._get_filter_func(file_extension)

    def __call__(self, filename):
        return self.filter_func(filename)

    def _get_filter_func(self, file_extension):
        return lambda filename: filename.endswith(file_extension)


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

    def _get_codebase_nodes(self, files_syntax_trees):
        for tree in files_syntax_trees:
            for node in tree:
                yield node

    def get_codebase_tokens(self):
        codebase_files = self._find_files()
        codebase_syntax_trees = self._get_syntax_trees(codebase_files)

        return self._get_codebase_nodes(codebase_syntax_trees)


class TokenTypeFilter(object):

    def __init__(self, token_type):
        self.filter_func = self._get_filter_func(token_type)

    def __call__(self, token):
        return self.filter_func(token)

    def _get_filter_func(self, token_type):
        if token_type == 'function':
            return lambda token: isinstance(token, ast.FunctionDef) and not \
                (token.name.startswith('__') and 
                 token.name.endswith('__'))
        else: return lambda token: False


class PartOfSpeechFilter(object):

    def __init__(self, part_of_speech):
        self.filter_func = self._get_filter_func(part_of_speech)

    def __call__(self, word):
        return self.filter_func(word)

    def _get_filter_func(self, part_of_speech):
        def _is_target_part_of_speech(word=''):
            if not word:
                return False
            pos_info = nltk.pos_tag([word])
            word_tag = pos_info[0][1]
            return word_tag.startswith(part_of_speech)

        return _is_target_part_of_speech


class CodeBaseAnalizer(object):
    """ Analize collected codebase data """

    def __init__(self, codebase_tokens,
                 target_token_type='function',
                 target_part_of_speech='VB'):
        self._codebase_tokens = codebase_tokens
        self._filter_token = TokenTypeFilter(target_token_type)
        self._filer_part_of_speech = PartOfSpeechFilter(target_part_of_speech)

    def __str__(self):
        return 'Analize codebase tokens {0}'.format(self._codebase_tokens)

    def _get_codebase_tokens_names(self):
        for token in filter(self._filter_token, self._codebase_tokens):
            yield token.name.lower()

    def _get_codebase_words(self, codebase_tokens_names):
        for token_name in codebase_tokens_names:
            for word in filter(self._filer_part_of_speech,
                               token_name.split('_')):
                yield word

    def _get_top_words(self, words, top_size):
        return collections.Counter(words).most_common(top_size)

    def find_top_codebase_words(self, top_size):
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
        total_verbs_count = sum(word_occurance for
                                word, word_occurance in self._popular_words)
        unique_verbs_count = len(self._popular_words)

        return total_verbs_count, unique_verbs_count, self._popular_words


class CodeBaseReportService(object):  # pragma: no cover
    """ Display code base report """

    def __init__(self, report_data):
        self._report_data = report_data

    def show_top_verbs_report(self):
        total_verbs_count, unique_verbs_count, popular_words_counter = \
            self._report_data
        for verb, verb_occurence in popular_words_counter:
            print('Verb "{0}" occured {1} times'.format(verb, verb_occurence))
        print('Total verbs {0}; unique verbs {1}'.format(total_verbs_count,
                                                         unique_verbs_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find most popular words in your codebase.')
    parser.add_argument('path', type=str,
                        help='root path of your project')
    parser.add_argument('--ext', type=str, default='.py',
                        help='files extension you want to analize')
    parser.add_argument('--top-size', type=int, default=10,
                        help='how long top list would you like to see?')
    parser.add_argument('--show-progress', action='store_true',
                        help='do you want to see progress bar?')
    args = parser.parse_args()

    codebase_parser = CodeBaseParser(args.path, args.ext,
                                     args.show_progress)
    codebase_tokens = codebase_parser.get_codebase_tokens()

    codebase_analizer = CodeBaseAnalizer(codebase_tokens)
    popular_words = codebase_analizer.find_top_codebase_words(args.top_size)

    report_data_generator = ReportDataGenerator(popular_words)
    report_data = report_data_generator.generate_report_data()

    codebase_reporter = CodeBaseReportService(report_data)
    codebase_reporter.show_top_verbs_report()
