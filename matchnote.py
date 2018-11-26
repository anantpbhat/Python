#!/usr/bin/env python3

import re
import argparse

parser = argparse.ArgumentParser(description="Match note from a magazine.")
parser.add_argument("--mag", metavar="", help="Specify magazine sentence here.")
parser.add_argument("--note", metavar="", help="Specify note.")
args = parser.parse_args()

MISS = 0
qp = re.compile(r'^q$|^quit$', re.I)

def quitout(qarg):
    if qp.search(qarg):
        print("Quiting at users request...")
        exit(0)

if args.mag or args.note:
    MGIN = args.mag
    NTIN = args.note
else:
    MGIN = input("Enter Magazine sentence or (q|Q) to quit: ")
    quitout(MGIN)
    NTIN = input("Enter Note or (q|Q) to quit: ")
    quitout(NTIN)

MGARY = list(MGIN.strip().split())
NTARY = list(NTIN.strip().split())

for i in NTARY:
    if i in MGARY:
        MGARY.remove(i)
    else:
        MISS += 1
        print("Some word[s] from Note are missing in magazine.")
        break

if MISS == 0:
    print("All words from Note found in magazine.")

