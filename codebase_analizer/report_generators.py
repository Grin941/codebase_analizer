"""
Module generates report (writes it to the specific stdout).
:param report_data: collections.namedtuple(
    'ReportData',
    ['total_words_count', 'unique_words_count', 'popular_words']
 )

"""
import os
import json
import csv


def generate_stdout_report(report_data):
    """
    Print report to the stdout
    """
    total_words_count, unique_words_count, \
        popular_words_counter = report_data
    for word, word_occurence in popular_words_counter:
        print('Word "{0}" occured {1} times'.format(word, word_occurence))
    print('Total words {0}; unique words {1}'.format(total_words_count,
                                                     unique_words_count))


def generate_csv_report(report_data):
    """
    Generate CSV report file
    """
    home_dir = os.path.expanduser('~')
    report_file = os.path.join(home_dir, 'codebase_report.csv')

    with open(report_file, 'w', encoding='utf-8') as csvfile:
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

        print('Report {0} generated'.format(report_file))


def generate_json_report(report_data):
    """
    Generate report as .json file
    """
    home_dir = os.path.expanduser('~')
    report_file = os.path.join(home_dir, 'codebase_report.json')

    with open(report_file, 'w', encoding='utf-8') as jsonfile:
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
        print('Report {0} generated'.format(report_file))
