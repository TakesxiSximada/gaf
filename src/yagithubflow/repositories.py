import re

import git

from yagithubflow.exc import NoRepositoryError

# git@github.org:UserName/RepositoryName.git
regx_ssh = re.compile(r'^git@github.com:(?P<org>[^/]+)/(?P<repo>.*).git')


class Repository:
    def __init__(self, local, remote):
        self.local = local
        self.remote = remote


def get_repository(github):
    local = git.Repo(search_parent_directories=True)
    origin = local.remote('origin')
    for url in origin.urls:
        matching = regx_ssh.match(url)
        if matching:
            org_name = matching.group('org')
            repo_name = matching.group('repo')
            remote = github.repository(org_name, repo_name)
            return Repository(local, remote)
    raise NoRepositoryError()
