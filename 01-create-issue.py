#! /usr/bin/env python
"""
eval "$(hub alias -s)"
git issue create -m "test"
"""
import sys
from subprocess import (
    PIPE,
    Popen,
    STDOUT,
    )

cmd = ['hub', 'issue', 'create'] + sys.argv[1:]

child = Popen(cmd, stdout=PIPE, stderr=STDOUT)
stdout, stderr = child.communicate()
issue_url = stdout.decode().strip()
issue_id = int(issue_url.split('/')[-1])

cmd = ['git', 'checkout', '-b', ]
child = Popen(cmd, stdout=PIPE, stderr=STDOUT)
stdout, stderr = child.communicate()
