import collections

# Python 2/3 compatibility
from builtins import object

from .report_generators import StdoutReportGenerator, \
    CsvReportGenerator, JsonReportGenerator


ReportData = collections.namedtuple(
    'ReportData', ['total_words_count', 'unique_words_count', 'popular_words']
)


def generate_report_data(popular_words):
    total_words_count = sum(word_occurance for
                            word, word_occurance in popular_words)
    unique_words_count = len(popular_words)

    return ReportData(
        total_words_count, unique_words_count, popular_words
    )


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
