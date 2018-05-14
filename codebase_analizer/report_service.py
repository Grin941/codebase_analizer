import collections

from .report_generators import StdoutReportGenerator, \
    CsvReportGenerator, JsonReportGenerator


ReportData = collections.namedtuple(
    'ReportData', ['total_words_count', 'unique_words_count', 'popular_words']
)

REPORT_GENERATOR_FACTORY = {
    'stdout': StdoutReportGenerator,
    'csv': CsvReportGenerator,
    'json': JsonReportGenerator,
}


def _generate_report_data(popular_words):
    total_words_count = sum(word_occurance for
                            word, word_occurance in popular_words)
    unique_words_count = len(popular_words)

    return ReportData(
        total_words_count, unique_words_count, popular_words
    )


def show_top_words_report(popular_words, user_settings):
    """ Display code base report """
    report_format = user_settings.report_format
    report_data = _generate_report_data(popular_words)
    report_generator = REPORT_GENERATOR_FACTORY.get(
        report_format, StdoutReportGenerator)(report_format)

    report_generator.generate_report(report_data)
