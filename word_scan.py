import argparse
import re

parser = argparse.ArgumentParser(description="Scan words from User Input file or specified argument file.")
parser.add_argument("-i", "--infile", metavar="", help="Specify a word File to scan")
args = parser.parse_args()

qp = re.compile(r'^q$|^quit$', re.I)


def count_lines_words(arg1, lcnt):
    with open(arg1, 'r') as wrdfile:
        print("Filename to scan is: " + wrdfile.name, "\n")
        for ln in wrdfile.readlines():  # type: str
            wrds = ln.split()
            print("Line", lcnt, "has", len(wrds), "words")
            lcnt += 1

def quitout(qarg, ec):
    if qp.search(qarg):
        print("Quiting at users request...")
        exit(code=ec)

if args.infile:
    INFILE = args.infile
else:
    INFILE = input("Type in a Filename to scan or (q|Q) to quit: ")
    quitout(INFILE, 1)

count_lines_words(INFILE, 1)
print("")

while True:
    sword = input("Type in a word to scan in this input file or (q|Q) to quit: ")
    quitout(sword, 0)
    wp = re.compile(r'\b' + sword + r'\b', re.I)
    cnt, lary = 1, []
    with open(INFILE, 'r') as file1:
     for l in file1.readlines():
        if wp.search(l):
            lary.append(cnt)
        cnt += 1
    if len(lary) > 0:
        rpwrd = len(lary) - 1
        print("Found word:", sword, "1st in line:", lary[0], "and is repeated again", rpwrd, "time(s) in this file.")
    else:
        print("Word ", sword, "not found in this file.")
exit(code=0)
