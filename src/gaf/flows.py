import os
import re
import logging

import github3.exceptions

from gaf.labels import Label
from gaf.exc import (
    DuplicateReealseError,
    GafError,
    )


logger = logging.getLogger(__name__)


def get_version(branch_name):
    # branch_name = local.head.ref.name
    return branch_name.lstrip('release-').split('-')[0]


def get_issue_id(branch_name):
    return int(branch_name.split('-')[1])


def get_pullrequest_id(url):
    return int(re.search('(?P<id>\d+)$', url).group('id'))


def build_branch_name(name, number, title):
    branch_name = '{}-{}-{}'.format(
        name, number, re.sub('[^\w]', '', title)[:10])
    return branch_name


def get_flow(repo, name='general'):
    if name == 'general':
        return Flow(repo)
    elif name == 'release':
        return ReleaseFlow(repo)
    elif name == 'hotfix':
        return HotfixFlow(repo)


class Flow(object):
    def __init__(self, repo):
        self.repo = repo

    def init(self):
        remote = self.repo.remote

        already_exist_labels = [
            label.name for label in remote.labels()]

        for label in Label.all():
            if label.name not in already_exist_labels:
                logger.debug('Create label: repo={}, label={}'.format(
                    remote, label))
                remote.create_label(label.name, label.color)
                yield label

    def create(self, title):
        local = self.repo.local
        remote = self.repo.remote
        github = self.repo.github

        me = github.me()
        local.git.fetch('origin')
        issue = remote.create_issue(title=title)

        branch_name = build_branch_name(
            me.name, issue.number, title)

        local.git.checkout('origin/master', b=branch_name)
        local.git.push('origin', branch_name, set_upstream=True)
        return issue

    def fix(self, title):
        local = self.repo.local
        remote = self.repo.remote

        os.system('git rebase -i origin/master')
        branch_name = local.head.ref.name
        issue_id = get_issue_id(branch_name)
        issue = remote.issue(issue_id)
        os.system('git commit --amend -m "{}"'.format(
            title + ' fixes #{}'.format(issue_id)))
        local.git.push('origin', branch_name, force=True)

        for retry in range(5):  # retry count
            try:
                pullreq = remote.create_pull(title, 'master', branch_name)
                pullreq.update(body='See {}'.format(issue.html_url))
                return pullreq
            except github3.exceptions.UnprocessableEntity:
                logger.exception('Cannot create pullrequest: retry={}'.format(retry))
                continue
        print('Already create pullrequest or other error: branch={}'.format(branch_name))


class ReleaseFlow(object):
    def __init__(self, repo):
        self.repo = repo

    def draft(self, version, title, prerelease=False):
        local = self.repo.local
        remote = self.repo.remote

        branch_name = build_branch_name(
            'release', version, title)
        local.git.checkout('origin/master', b=branch_name)
        local.git.commit(message='release draft {}'.format(version), allow_empty=True)
        local.git.push('origin', branch_name, set_upstream=True)
        pullreq = remote.create_pull(
            'Release {} - {}'.format(version, title),
            'master', branch_name)

        for release in remote.releases():
            if release.name == version:
                raise DuplicateReealseError('duplicated: {}, {}'.format(
                    version, release.url))

        release = remote.create_release(
            tag_name=version, target_commitish=branch_name,
            name=version, draft=True, prerelease=prerelease)
        pullreq.update(body='Release {}'.format(release.html_url))
        pullreq.issue().add_labels(Label.release.name)
        return pullreq

    def list_(self):
        os.system('git branch | grep release')

    def merge(self, url):
        os.system('hub am -3 {}'.format(url))

    def accept(self, url):
        local = self.repo.local
        remote = self.repo.remote
        version = get_version(local.head.ref.name)

        pull_request_id = get_pullrequest_id(url)
        pr = remote.pull_request(pull_request_id)

        # commits = [commit for commit in pr.commits()]
        # commit = commits[0]
        # author = commit.author.refresh()
        # os.system("git commit --amend --author '{} <{}>' ".format(
        #     author.name, author.email,
        #     ))

        accept_message = (
            'Thanks!! '
            'This pull request is merged. '
            'Until the new version {} is released, '
            'please wait for a while.'
            ).format(version)

        issue = pr.issue()
        issue.add_labels(Label.accept.name)

        local.remote().push()

        pr.create_comment(accept_message)
        pr.close()

        local.delete_head(pr.head.ref)
        local.remote().push(pr.head.ref, delete=True)

    def reject(self):
        pass

    def be_rebase(self):
        pass

    def be_squash(self):
        pass

    def clean(self):
        local = self.repo.local

        if not local.head.ref.name.startswith('release-'):
            raise GafError('not release branch')

        os.system('git rebase -i origin/master')
        local.remote().push(force=True)

    def publish(self, version_or_url):
        local = self.repo.local
        remote = self.repo.remote

        if version_or_url.startswith('https'):
            pull_request_id = get_pullrequest_id(version_or_url)
            pullreq = remote.pull_request(pull_request_id)
            version = get_version(pullreq.head.ref)
        else:
            version = version_or_url
            for pr in remote.pull_requests():
                if pr.head.ref == local.head.ref.name:
                    pullreq = pr
                    break

        if pullreq is None:
            raise GafError('No release pull request')

        elif pullreq.head.ref != local.head.ref.name:
            raise GafError('Branch Mismatch: {} != {}'.format(
                pullreq.head.ref, local.head.ref.name))

        elif version != get_version(local.head.ref.name):
            raise GafError('Version Mismatch')

        release = None
        for remote_release in remote.releases():
            if remote_release.name == version:
                release = remote_release
                break
        if release is None:
            raise GafError('Release not found')

        issue = pullreq.issue()
        issue.add_labels(Label.accept.name)

        local.git.checkout('master')
        self.merge(pullreq.html_url)  # master merge
        pullreq.close()

        local.delete_head(pullreq.head.ref)
        local.remote().push(pullreq.head.ref, delete=True)

        tag = local.create_tag(version)
        local.remote().push()
        local.remote().push(tags=True)

        release.edit(draft=False, tag_name=tag.name)

        pullreq.create_comment('Released!! {}'.format(release.html_url))
        return release


class HotfixFlow(object):
    def __init__(self, repo):
        self.repo = repo

    def create(self):
        pass

    def accept(self):
        pass
