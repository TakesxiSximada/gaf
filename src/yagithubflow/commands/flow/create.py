import re
import sys
import logging
import argparse

from yagithubflow.bootstraps import bootstrap
from yagithubflow.exc import AuthTokenCreationError
from yagithubflow.repositories import get_repository

logger = logging.getLogger(__name__)


def create_issue(github, title):
    repo = get_repository(github)
    me = github.me()
    repo.local.git.fetch('origin')

    issue = github.create_issue(
        owner=me.name, repository=repo.remote.name, title=title)
    branch_name = '{}-{}-{}'.format(
        me.name, issue.number, re.sub('[^\w]', '', title)[:10])

    repo.local.git.checkout('origin/master', b=branch_name)
    repo.local.git.push('origin', branch_name, set_upstream=True)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('title')
    args = parser.parse_args(argv)
    title = args.title

    try:
        github = bootstrap()
    except AuthTokenCreationError:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1

    create_issue(github, title=title)


if __name__ == '__main__':
    sys.exit(main())
