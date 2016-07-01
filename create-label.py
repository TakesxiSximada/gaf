import re
import getpass

import git
import github3
import pit

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

gh = github3.login(
    username, password,
    two_factor_callback=get_two_factor_authentication_code,
    )

auth = gh.authorize(
    username, password, scopes=['user', 'repo'],
    note='yagithubflow', note_url='http://localhost',
    )
print(auth)
print(auth.token)
print(auth.id)

github = github3.login(token=auth.token)
# auth_obj = github.authorization(auth.id)
# auth_obj.update(add_scopes=['repo:status'], rm_scopes=['user'])

repo = git.Repo(search_parent_directories=True)
origin = repo.remote('origin')
url = None
for url in origin.urls:
    break
if url is None:
    raise ValueError()


regx_ssh = re.compile(r'^git@github.com:(?P<org>[^/]+)/(?P<repo>.*).git')
matching = regx_ssh.match(url)
if not matching:
    raise ValueError()

org_name = matching.group('org')
repo_name = matching.group('repo')
repo = github.repository(org_name, repo_name)

already_labels = [label.name for label in repo.labels()]
labels = ['ACCEPT', 'LGTM']
color = '0a0a11'
for label in labels:
    if label not in already_labels:
        labelobj = repo.create_label(label, color)
