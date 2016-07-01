import sys
import logging
import argparse

from gaf.bootstraps import bootstrap

logger = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('version_or_url', nargs='?', default=None)
    args = parser.parse_args(argv)
    version_or_url = args.version_or_url

    flow = bootstrap('release')
    if flow is None:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1
    flow.clean()

if __name__ == '__main__':
    sys.exit(main())
