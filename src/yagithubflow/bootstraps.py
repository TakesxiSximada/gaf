import os
import logging

import github3
import github3.exceptions

from .exc import AuthTokenCreationError
from .auths import (
    load_auth_token,
    create_auth_token,
    AUTH_TOKEN_FILE,
    )

logger = logging.getLogger(__name__)


def bootstrap():
    if os.path.exists(AUTH_TOKEN_FILE):
        auth = load_auth_token(AUTH_TOKEN_FILE)
    else:
        try:
            auth = create_auth_token(AUTH_TOKEN_FILE)
        except github3.exceptions.UnprocessableEntity as err:
            logger.exception('Cannot create auth token: %s', err)
            raise AuthTokenCreationError()
    return github3.login(token=auth.token)
