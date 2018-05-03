import pytest

from codebase_analizer.report_service import ReportDataGenerator


@pytest.fixture
def popular_words():
    return (('get', 10), ('find', 5), ('set', 8))


def test_report_data_generator_returns_total_unique_words_count_and_words(
    popular_words
):
    report_data_generator = ReportDataGenerator(popular_words)
    assert report_data_generator.generate_report_data() == \
        (23, 3, popular_words)
