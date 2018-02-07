import ast
import os
import collections
import nltk
import argparse

from tqdm import tqdm as progress_bar

# Python 2/3 compatibility
from io import open
from builtins import object


class CodeBaseAnalizer(object):
    """ Traverse and collect codebase data """

    def __init__(self, path, files_extension='.py', show_progress=False):
        self._path = path
        self._files_extension = files_extension
        self._show_progress = progress_bar if show_progress else lambda x: x

    def __str__(self):
        return 'Analize code base from {0}'.format(self._path)

    def _is_verb(self, word):
        if not word:
            return False
        pos_info = nltk.pos_tag([word])
        word_tag = pos_info[0][1]
        return word_tag.startswith('VB')

    def _find_files(self):
        for dirpath, dirnames, filenames in \
                self._show_progress(os.walk(self._path)):
            for filename in filenames:
                yield os.path.join(dirpath, filename)

    def _filter_files(self, files):
        for _file in files:
            if _file.endswith(self._files_extension):
                yield _file

    def _get_syntax_trees(self, files):
        for _file in files:
            file_content = open(_file, 'r', encoding='utf-8').read()
            try:
                parsed_file_content = ast.parse(file_content)
                yield ast.walk(parsed_file_content)
            except (SyntaxError, TypeError):
                pass

    def _get_func_names(self, files_syntax_trees):
        for tree in files_syntax_trees:
            for node in tree:
                if isinstance(node, ast.FunctionDef) and not \
                   (node.name.startswith('__') and node.name.endswith('__')):
                    yield node.name.lower()

    def _get_verbs_from_function_name(self, function_names):
        for function_name in function_names:
            for word in function_name.split('_'):
                if self._is_verb(word):
                    yield word

    def _get_top_verbs(self, verbs, top_size):
        return collections.Counter(verbs).most_common(top_size)

    def find_top_words(self, top_size):
        files_traversed = self._find_files()
        filtered_files = self._filter_files(files_traversed)
        syntax_trees = self._get_syntax_trees(filtered_files)
        function_names = self._get_func_names(syntax_trees)
        function_name_verbs = self._get_verbs_from_function_name(
            function_names)

        return self._get_top_verbs(function_name_verbs, top_size)


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


class CodeBaseReportService(object):
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
    parser.add_argument('--top_size', type=int, default=10,
                        help='how long top list would you like to see?')
    parser.add_argument('--show_progress', action='store_true',
                        help='do you want to see progress bar?')
    args = parser.parse_args()

    codebase_analizer = CodeBaseAnalizer(args.path, args.ext,
                                         args.show_progress)
    popular_words = codebase_analizer.find_top_words(args.top_size)

    report_data_generator = ReportDataGenerator(popular_words)
    report_data = report_data_generator.generate_report_data()

    codebase_reporter = CodeBaseReportService(report_data)
    codebase_reporter.show_top_verbs_report()
