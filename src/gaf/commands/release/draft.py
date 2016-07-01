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
    parser.add_argument('version')
    parser.add_argument('-m', dest='title', default='notitle')
    parser.add_argument('--pre', dest='prerelease', default=False, action='store_true')
    args = parser.parse_args(argv)
    version = args.version
    title = args.title
    prerelease = args.prerelease

    flow = bootstrap('release')
    if flow is None:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1
    pullreq = flow.draft(version=version, title=title, prerelease=prerelease)
    print(pullreq.html_url)

if __name__ == '__main__':
    sys.exit(main())
