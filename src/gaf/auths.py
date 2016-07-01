import os
import logging
import getpass

import six
import github3
import github3.exceptions

logger = logging.getLogger(__name__)

AUTH_TOKEN_FILE = os.path.join(
    os.path.expanduser('~'),
    '.gaf',
    'auth_token.json',
    )


def get_two_factor_authentication_code():
    while True:
        code = getpass.getpass('Code (see your mobile phone):')
        if code:
            return code


def create_auth_token_directory(path=AUTH_TOKEN_FILE):
    auth_token_dir = os.path.dirname(path)
    if not os.path.exists(auth_token_dir):
        os.makedirs(auth_token_dir, exist_ok=True)


def create_auth_token(path=AUTH_TOKEN_FILE):
    create_auth_token_directory(path)
    username = six.moves.input('username: ')
    password = getpass.getpass('password:')

    auth = github3.authorize(
        username, password, scopes=['repo'],
        note='gaf', note_url='http://localhost',
        two_factor_callback=get_two_factor_authentication_code,
        )
    with open(path, 'wb') as fp:
        buf = auth.as_json().encode()
        fp.write(buf)
    return auth


def load_auth_token(path=AUTH_TOKEN_FILE):
    with open(path, 'rb') as fp:
        buf = fp.read().decode()
        return github3.auths.Authorization.from_json(buf)
