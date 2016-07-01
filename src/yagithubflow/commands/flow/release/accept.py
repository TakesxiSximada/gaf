import sys
from yagithubflow import bootstrap


def main(argv=sys.argv[1:]):
    flow = bootstrap()
    release = flow.release
    return release.accept()

if __name__ == '__main__':
    sys.exit(main())
