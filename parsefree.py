#!/usr/bin/env python3.6

import re
import argparse
from subprocess import run, PIPE
from time import sleep

parser = argparse.ArgumentParser(description="Parse Free cmd in a loop.")
parser.add_argument("-i", "--interval", metavar="", help='Specify interval in secs. Only +ve numbers allowed.')
parser.add_argument("-c", "--count", metavar="", help='Specify count. Only +ve numbers allowed.')
args = parser.parse_args()

fmp = re.compile(r'^Mem:\s+')
fswp = re.compile(r'^Swap:\s+')

if args.interval:
    intvl = int(args.interval)
else:
    intvl = 5

if args.count:
    cnt = int(args.count)
else:
    cnt = 3

while cnt > 0:
    frout = run(["free -h"], shell=True, stdout=PIPE)
    frout_string = frout.stdout.decode('utf-8').strip()
    frlines = frout_string.split("\n")
    print("ResName\tTotal \t Used \t Free")
    for ln in frlines:
        if fmp.search(ln):
            ln = ln.split()
            print("Memory\t", ln[1], "\t", ln[2], "\t", ln[6])
            continue
        if fswp.search(ln):
            ln = ln.split()
            print("Swap\t", ln[1], "\t", ln[2], "\t", ln[3])
    cnt -= 1
    if cnt != 0:
        sleep(intvl)
        print()
