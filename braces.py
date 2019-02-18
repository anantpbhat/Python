#!/usr/bin/env python3.6

import re, argparse

parser = argparse.ArgumentParser(description="Script to check braces in a code.")
parser.add_argument("-i", "--usrin", metavar="", help="Provide input with braces, brackets or parentheses")
args = parser.parse_args()

qp = re.compile(r'^q$|^quit$', re.I)
brp = re.compile(r'\}|\)|\]')
bary = []
USERIN = ""

def quitout(qarg, qc):
    print(qarg)
    exit(code=qc)

if args.usrin:
    USERIN = args.usrin

while True:
    if not USERIN: USERIN = input("Enter Input: ")
    if qp.search(USERIN): quitout("Quiting at users request...", 0)

    if brp.search(USERIN[0]):
        print("Syntax error found in enclosures. Bad Code!!!")
        USERIN = ""
        continue

    for i in USERIN:
        if i == "{":
            bary.insert(0, "}")
            continue
        elif i == "[":
            bary.insert(0, "]")
            continue
        elif i == "(":
            bary.insert(0, ")")
            continue
        elif brp.search(i) and len(bary) != 0 and i == bary[0]:
            del bary[0]
            continue
        elif brp.search(i):
            bary.insert(0, i)
            break
        else: quitout("Invalid character in input. Quiting...", 2)

    if len(bary) == 0:
        print("Enclosures check Passed, Code is compliant.")
    else:
        print("Syntax error found in enclosures. Bad Code!!!")

    USERIN = ""
