import sys
from yagithubflow import bootstrap


def main(argv=sys.argv[1:]):
    flow = bootstrap()
    return flow.fix()

if __name__ == '__main__':
    sys.exit(main())
