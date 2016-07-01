import os
import logging

import github3
import github3.exceptions

from .exc import (
    AuthTokenCreationError,
    GafError,
    )
from .flows import get_flow
from .repositories import get_repository


from .auths import (
    load_auth_token,
    create_auth_token,
    AUTH_TOKEN_FILE,
    )

logger = logging.getLogger(__name__)


def bootstrap(name='general', raise_exception=False):
    try:
        github = get_github()
        repo = get_repository(github)
        flow = get_flow(repo, name)
        return flow
    except GafError as err:
        if raise_exception:
            raise
        else:
            logger.debug('Bootstrap error: %s', err)
            return None


def get_github():
    if os.path.exists(AUTH_TOKEN_FILE):
        auth = load_auth_token(AUTH_TOKEN_FILE)
    else:
        try:
            auth = create_auth_token(AUTH_TOKEN_FILE)
        except github3.exceptions.UnprocessableEntity as err:
            logger.exception('Cannot create auth token: %s', err)
            raise AuthTokenCreationError()
    return github3.login(token=auth.token)
