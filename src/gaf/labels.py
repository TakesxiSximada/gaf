class _Label:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        return '{} ({})'.format(self.name, self.color)


class Label:
    accept = _Label('ACCEPT', '298A08')
    reject = _Label('REJECT', '610B38')
    squash = _Label('SQUASH', 'B82100')
    rebase = _Label('REBASE', 'CA8204')
    release = _Label('RELEASE', 'CA8204')

    @classmethod
    def all(cls):
        yield cls.accept
        yield cls.reject
        yield cls.squash
        yield cls.rebase
        yield cls.release
