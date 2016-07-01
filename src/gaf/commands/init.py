import sys
import logging

from gaf.bootstraps import bootstrap

logger = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    flow = bootstrap()
    if flow is None:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1

    for label in flow.init():
        print('Create label: {} {}'.format(label.name, label.color))

if __name__ == '__main__':
    sys.exit(main())
