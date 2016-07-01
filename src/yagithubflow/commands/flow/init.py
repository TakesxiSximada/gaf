import sys
import logging

from yagithubflow.bootstraps import bootstrap
from yagithubflow.exc import AuthTokenCreationError
from yagithubflow.labels import Label
from yagithubflow.repositories import get_repository

logger = logging.getLogger(__name__)


def create_labels(github):
    repo = get_repository(github)

    already_exist_labels = [label.name for label in repo.remote.labels()]

    for label in Label.all():
        if label.name not in already_exist_labels:
            print('Create label: repo={}, label={}'.format(repo.remote, label))
            repo.create_label(label.name, label.color)


def main(argv=sys.argv[1:]):
    try:
        github = bootstrap()
    except AuthTokenCreationError:
        print(
            'Cannot create auth token: Does it have already been created? '
            'See https://github.com/settings/tokens'
            )
        return 1
    create_labels(github)


if __name__ == '__main__':
    sys.exit(main())
