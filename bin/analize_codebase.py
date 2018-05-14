import argparse

from codebase_analizer import \
    Project, \
    codebase_parser, \
    codebase_analizer, \
    report_service


def parse_user_settings():
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
    parser.add_argument('--show-progress', action='store_false',
                        help='do you want to see progress bar?')
    return parser.parse_args()


def main():  # pragma: no cover
    user_settings = parse_user_settings()

    project = Project(user_settings.project_location)

    with project.open() as project_path:
        codebase_tokens = codebase_parser.get_codebase_tokens(
            project_path,
            user_settings
        )
        popular_words = codebase_analizer.find_top_codebase_words(
            codebase_tokens,
            user_settings
        )
        report_service.show_top_words_report(
            popular_words,
            user_settings
        )


if __name__ == '__main__':
    main()
