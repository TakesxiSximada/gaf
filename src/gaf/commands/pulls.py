import sys
import logging
import argparse

from gaf.bootstraps import bootstrap

logger = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    args = parser.parse_args(argv)  # noqa

    flow = bootstrap()
    if flow is None:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1

    for pullreq in flow.pullrequests():
        print('{} : {}'.format(pullreq.html_url, pullreq.title))


if __name__ == '__main__':
    sys.exit(main())
