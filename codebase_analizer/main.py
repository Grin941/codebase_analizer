import argparse

from codebase_analizer import parsers as codebase_parser
from .report_service import CodeBaseReportService, \
    ReportDataGenerator
from codebase_analizer import analizer as codebase_analizer
from .project import Project


parser = argparse.ArgumentParser(
    description='Find most popular words in your codebase.')
parser.add_argument('project_location', type=str,
                    help="""root path of your project or
                            url to clone the repo from""")
parser.add_argument('--files-ext', default='.py', const='.py',
                    nargs='?', choices=['.py', ],
                    help="""files extension you want to analize
                            (default: %(default)s)""")
parser.add_argument('--token-type', default='function', const='function',
                    nargs='?', choices=['function', 'variable'],
                    help="""what token type do you want to analize:
                            function or variable
                            (default: %(default)s)?""")
parser.add_argument('--part-of-speech', default='VB', const='VB',
                    nargs='?', choices=['VB', 'NN'],
                    help="""what type of speech do you want to analize:
                            verb or noun
                            (default: %(default)s)?""")
parser.add_argument('--report-format', default='stdout', const='stdout',
                    nargs='?', choices=['stdout', 'csv', 'json'],
                    help="""how do you want to see your report:
                            print to stdout or generate json/scv file
                            (default: %(default)s)?""")
parser.add_argument('--top-size', type=int, default=10,
                    help="""how long top list would you like to see
                            (default: %(default)s)?""")
parser.add_argument('--show-progress', action='store_true',
                    help='do you want to see progress bar?')


def run():  # pragma: no cover
    user_settings = parser.parse_args()

    project = Project(user_settings.project_location)
    if project.should_be_clonned:
        project.clone()

    codebase_tokens = codebase_parser.get_codebase_tokens(
        project.path,
        **user_settings
    )
    popular_words = codebase_analizer.find_top_codebase_words(
        codebase_tokens,
        **user_settings
    )

    report_data_generator = ReportDataGenerator(popular_words)
    report_data = report_data_generator.generate_report_data()

    codebase_reporter = CodeBaseReportService(report_data,
                                              args.report_format)
    codebase_reporter.show_top_words_report()

    if project.should_be_clonned:
        # Remove clonned project -
        # user should not store folders he don't know about.
        project.remove()
