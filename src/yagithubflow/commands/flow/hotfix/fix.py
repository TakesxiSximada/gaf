import sys
from yagithubflow import bootstrap


def main(argv=sys.argv[1:]):
    flow = bootstrap()
    hotfix = flow.hotfix
    return hotfix.fix()

if __name__ == '__main__':
    sys.exit(main())
