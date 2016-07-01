"""
- コミットをスカッシュ `git rebase -i origin/master`
- コミットメッセージにfixesを追加
- push -f
- git pull-request -m "pull request title"
"""
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
    pr = flow.fix(title=title)
    if pr:
        print('Create pullrequest: {}'.format(pr.url))


if __name__ == '__main__':
    sys.exit(main())
