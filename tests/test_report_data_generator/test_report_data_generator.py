from codebase_analizer import report_service


def test_report_data_generator_returns_total_unique_words_count_and_words(
    popular_words
):
    assert report_service._generate_report_data(popular_words) == \
        (23, 3, popular_words)
