import collections

from codebase_analizer import report_generators

ReportData = collections.namedtuple(
    'ReportData', ['total_words_count', 'unique_words_count', 'popular_words']
)

REPORT_GENERATOR_FACTORY = {
    'stdout': report_generators.generate_stdout_report,
    'csv': report_generators.generate_csv_report,
    'json': report_generators.generate_json_report,
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
    generate_report = REPORT_GENERATOR_FACTORY.get(report_format)

    generate_report(report_data)
