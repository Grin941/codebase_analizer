# Python 2/3 compatibility
from builtins import object

from report_generators import StdoutReportGenerator, \
    CsvReportGenerator, JsonReportGenerator


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
