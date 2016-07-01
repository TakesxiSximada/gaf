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

scopes = ['repo']
note = 'yagithubflow'
note_url = 'http://localhost'
two_factor_callback = get_two_factor_authentication_code


# auth = github3.authorize(
#     username, password, scopes=scopes, note=note, note_url=note_url,
#     two_factor_callback=two_factor_callback,
#     )

# with open('.auth.json', 'wb') as fp:
#     fp.write(auth.as_json().encode())

with open('.auth.json', 'rb') as fp:
    buf = fp.read().decode()
    auth = github3.auths.Authorization.from_json(buf)


gh = github3.login(token=auth.token)
print(gh.meta())

# github = github3.login(
#     username, password,
#     two_factor_callback=get_two_factor_authentication_code)
# auth = github.authorize(
#     username, password, scopes=['user', 'repo'],
#     note='poi', note_url='http://localhost')
s
