from codebase_analize.report_service import ReportDataGenerator


class TestReportDataGenerator:
    def setup(self):
        self.popular_words = (('get', 10), ('find', 5), ('set', 8))

    def test_report_data_generator_returns_total_unique_words_count_and_words(self):
        report_data_generator = ReportDataGenerator(self.popular_words)

        assert report_data_generator.generate_report_data() == (23, 3, self.popular_words)
