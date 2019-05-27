#!/usr/bin/env python

import re
from subprocess import check_output, Popen, PIPE
from datetime import datetime

n = 1
cmd = ("/sbin/ip", "a")
goodp = re.compile("inet \d\d")
badp = re.compile("127.0.0.1")

out = check_output(cmd, universal_newlines=True)
for line in out.split("\n"):
    print(line)

with Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True) as proc:
    for line in proc.stdout.readlines():
        line = line.rstrip()
        if goodp.search(line):
            linelst = line.split()
            DT = str(datetime.now()).split()
            print("%s\tIP%d: %s\tPID: %d" % (DT[1], n, linelst[1], proc.pid))
            n += 1
