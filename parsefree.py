#!/usr/bin/env python3.6

import argparse, re
from time import sleep
from os import popen
from datetime import datetime

parser = argparse.ArgumentParser(description="Parse Free cmd in a loop.")
parser.add_argument("-i", "--interval", metavar="", help='Specify interval in secs. Only +ve numbers allowed.')
parser.add_argument("-c", "--count", metavar="", help='Specify count. Only +ve numbers allowed.')
args = parser.parse_args()

fmp = re.compile(r'^Mem:\s+')
fswp = re.compile(r'^Swap:\s+')

def getdt():
    dttm = datetime.now()
    dt = (str(dttm.year) + "-" + str(dttm.month) + "-" + str(dttm.day))
    tm = (str(dttm.hour) + ":" + str(dttm.minute) + ":" + str(dttm.second))
    return (dt, tm)

if args.interval:
    intvl = int(args.interval)
else:
    intvl = 5

if args.count:
    cnt = int(args.count)
else:
    cnt = 3

while cnt > 0:
    (DT, TM) = getdt()
    print("Date:", DT, "\t", "Time:", TM)
    print("ResName\tTotal \t Used \t Free")
    for ln in popen('free -h').readlines():
        ln.rstrip()
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
