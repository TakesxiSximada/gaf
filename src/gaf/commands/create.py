import sys
import logging
import argparse

from gaf.bootstraps import bootstrap

logger = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('title')
    args = parser.parse_args(argv)
    title = args.title

    flow = bootstrap()
    if flow is None:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1

    issue = flow.create(title=title)
    print('Create new issue: {}'.format(issue.url))

if __name__ == '__main__':
    sys.exit(main())
