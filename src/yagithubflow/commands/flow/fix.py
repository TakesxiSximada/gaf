"""
- コミットをスカッシュ `git rebase -i origin/master`
- コミットメッセージにfixesを追加
- push -f
- git pull-request -m "pull request title"
"""
import os
import sys
import logging
import argparse

import github3.exceptions

from yagithubflow.bootstraps import bootstrap
from yagithubflow.exc import AuthTokenCreationError
from yagithubflow.repositories import get_repository

logger = logging.getLogger(__name__)


def create_squashed_pullrequest(github, title):
    repo = get_repository(github)
    os.system('git rebase -i origin/master')
    branch_name = repo.local.head.ref.name
    issue_number = branch_name.split('-')[1]
    os.system('git commit --amend -m "{}"'.format(title + ' fixes #{}'.format(issue_number)))
    repo.local.git.push('origin', branch_name, force=True)
    try:
        repo.remote.create_pull(title, 'master', branch_name)
    except github3.exceptions.UnprocessableEntity:
        print('Already create pullrequest: branch={}'.format(branch_name))


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

    create_squashed_pullrequest(github, title=title)


if __name__ == '__main__':
    sys.exit(main())
