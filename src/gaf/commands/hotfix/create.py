import sys
from gaf import bootstrap


def main(argv=sys.argv[1:]):
    flow = bootstrap()
    hotfix = flow.hotfix
    return hotfix.create()

if __name__ == '__main__':
    sys.exit(main())
