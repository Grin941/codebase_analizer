import os
import json
import csv


__all__ = ['StdoutReportGenerator',
           'CsvReportGenerator',
           'JsonReportGenerator']


class ReportGenerator(object):

    def __init__(self, report_format):
        home_dir = os.path.expanduser('~')
        self._report_file = os.path.join(
            home_dir, 'codebase_report.{0}'.format(report_format))

    def generate_report(self, report_data):
        raise NotImplementedError('Should be implemented')


class StdoutReportGenerator(ReportGenerator):

    def generate_report(self, report_data):
        total_words_count, unique_words_count, \
            popular_words_counter = report_data
        for word, word_occurence in popular_words_counter:
            print('Word "{0}" occured {1} times'.format(word, word_occurence))
        print('Total words {0}; unique words {1}'.format(total_words_count,
                                                         unique_words_count))


class CsvReportGenerator(ReportGenerator):

    def generate_report(self, report_data):
        with open(self._report_file, 'w', encoding='utf-8') as csvfile:
            total_words_count, unique_words_count, \
                popular_words_counter = report_data

            csvwriter = csv.writer(csvfile, delimiter=';',
                                   quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # write fieldnames
            csvwriter.writerow(['Word', 'Occurance'])

            for word, word_occurence in popular_words_counter:
                csvwriter.writerow([word, word_occurence])

            # write result rows
            csvwriter.writerow(['Total words', total_words_count])
            csvwriter.writerow(['Unique words', unique_words_count])

            print('Report {0} generated'.format(self._report_file))


class JsonReportGenerator(ReportGenerator):

    def generate_report(self, report_data):
        with open(self._report_file, 'w', encoding='utf-8') as jsonfile:
            total_words_count, unique_words_count, \
                popular_words_counter = report_data

            report_dict = {}
            for word, word_occurence in popular_words_counter:
                report_dict[word] = word_occurence

            # write result rows
            results = report_dict['results']
            results['Total words'] = total_words_count
            results['Unique words'] = unique_words_count

            json.dump(report_dict, jsonfile)
            print('Report {0} generated'.format(self._report_file))
