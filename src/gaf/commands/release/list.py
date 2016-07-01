"""
- リリースブランチをmasterから作成 `git checkout -b release-VERSION origin/master`
- version番号をbump `make bumpversion VERSION`
"""
import sys
import logging
import argparse

from gaf.bootstraps import bootstrap

logger = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    args = parser.parse_args(argv)  # noqa

    flow = bootstrap('release')
    if flow is None:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1
    flow.list_()

if __name__ == '__main__':
    sys.exit(main())
