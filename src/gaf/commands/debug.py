import sys
import logging
import argparse

from gaf.bootstraps import bootstrap

logger = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('debugger', nargs='?', default='pdb')
    args = parser.parse_args(argv)  # noqa
    debugger = args.debugger

    flow = bootstrap()
    if flow is None:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1
    flow.debug(debugger=debugger)

if __name__ == '__main__':
    sys.exit(main())
