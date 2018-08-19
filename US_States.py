#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser(description="Enter a US State to get its Capital city or Vice-versa.")
parser.add_argument("-i", "--infile", metavar="", help="Specify US States/Capital file path")
args = parser.parse_args()

qp = re.compile(r'^q$|^quit$', re.I)

def mkdict(arg1, dict1):
    with open(arg1, 'r') as file1:
        file1_strip = (ln.strip() for ln in file1.readlines())
    for i in file1_strip:
        (a, b) = i.split(": ")
        dict1[a] = b
    return dict1

def getinput():
    IN1 = input("Enter a US State or Capital City or (q|Q) to quit: ")
    IN1 = IN1.title()
    return IN1

def checkinput(ec):
    for k, v in stdict.items():
        if userin == k:
            print("Capital City for US State -", k, "is:", stdict[k])
            ec = 0
            break
        elif userin == v:
            print(v, "is the Capital City for US State:", k)
            ec = 0
            break
        else:
            continue
    return ec

if args.infile:
    STFILE = args.infile
else:
    STFILE = "/home/abhat/States_Capital"

stdict = mkdict(STFILE, {})

while True:
    userin = getinput()
    if qp.search(userin):
        print("Exiting at users request...!")
        exit(0)
    rc = checkinput(1)
    if rc != 0:
        print("We noticed a BAD input from user.")
    print()
