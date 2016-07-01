import getpass

import pit
import github3

config = pit.Pit.get('releasemaster', {'require': {
    'username': 'YOUR GITHUB USERNAME',
    'password': 'YOUR GITHUB PASSWORD',
    }})

username = config['username']
password = config['password']


def get_two_factor_authentication_code():
    while True:
        code = getpass.getpass('Code (see your mobile phone):')
        if code:
            return code

scopes = ['user', 'repo']
note = 'yagithubflow'
note_url = 'http://localhost'
two_factor_callback = get_two_factor_authentication_code


gh = github3.login(
    username, password,
    two_factor_callback=two_factor_callback,
    )
import ipdb; ipdb.set_trace()
print(gh)
