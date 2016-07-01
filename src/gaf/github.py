class LabelFactory(object):
    def __init__(self, repo):
        self.repo = repo

    def __call__(self, name, color):
        remote = self.repo.remote
        remote.create_label(name, color)
