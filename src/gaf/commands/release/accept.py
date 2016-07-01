import sys
import logging
import argparse

from gaf.bootstraps import bootstrap

logger = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args(argv)
    url = args.url

    flow = bootstrap('release')
    if flow is None:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1
    flow.accept(url=url)

if __name__ == '__main__':
    sys.exit(main())
