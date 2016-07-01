import sys
from gaf import bootstrap


def main(argv=sys.argv[1:]):
    flow = bootstrap()
    release = flow.release
    return release.patch()

if __name__ == '__main__':
    sys.exit(main())
