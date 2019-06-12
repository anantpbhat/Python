#!/usr/bin/env python

import re
from subprocess import check_output, Popen, PIPE
from datetime import datetime

n = 1
cmd = ("/sbin/ip", "a")
cmd1 = ("/usr/bin/lshw", "-businfo", "-C", "network")
goodp = re.compile("inet \d\d")
badp = re.compile(r'(^Bus info)|(^===)')

out = check_output(cmd1, universal_newlines=True)
for line in out.split("\n"):
    print(line)

with Popen(cmd1, stdout=PIPE, stderr=PIPE, universal_newlines=True) as proc:
    for line in proc.stdout.readlines():
        line = line.rstrip()
        if badp.search(line) or line == "": continue
        linelst = line.split()
        desc = " ".join(linelst[3:])
        print("Network Device %d is: %s and is described as - %s" % (n, linelst[1], desc))
        n += 1
