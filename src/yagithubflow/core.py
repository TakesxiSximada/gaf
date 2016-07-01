import os
import getpass
import functools

import github3


get_home_dir = functools.partial(
    os.path.expanduser,
    '~',
    )


def get_auth_file_path():
    return os.path.join(
        get_home_dir(),
        '.yagithubflow/auth.json'
        )


def get_two_factor_authentication_code():
    while True:
        code = getpass.getpass('Code (see your mobile phone):')
        if code:
            return code


def get_session():
    auth_file_path = get_auth_file_path()
    if not os.path.exists(auth_file_path):
        os.makedirs(
            os.path.basename(auth_file_path),
            mode=0o700,
            exist_ok=True,
            )
        github3.authorize()
