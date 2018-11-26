#!/usr/bin/env python3.6

import argparse, re, os

class Argsnrgx():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Script to rotate logs for given input Log filename.")
        self.parser.add_argument("-l", "--logfile", metavar="", help="Specify Log filename")
        self.args = self.parser.parse_args()
        self.qp = re.compile(r'^q$|^quit$', re.I)

class Getfile(Argsnrgx):
    def chkargs(self):
        self.logfile = self.args.logfile

    def chkin(self):
        self.infile = input("Enter Log Filename: ")

    def quitout(self):
        print("Quiting at users request...")
        exit(code=0)

class ProgLgc():
    def crtlst(self, fl):
        self.fl = fl
        self.extnary = [int(x.split(".")[1]) for x in os.listdir(".") if x.startswith(self.fl + ".") and os.path.isfile(x)]
        self.extnary.sort(reverse=True)

    def rnm(self):
        for i in self.extnary:
            os.rename((self.fl + "." + str(i)), (self.fl + "." + str(i + 1)))
        os.rename(self.fl, self.fl + "." + "0")
        open(self.fl, 'a').close()                    # Touch a file, fl


if __name__ == "__main__":
    gtfl = Getfile()
    gtfl.chkargs()
    if gtfl.logfile:
        lfile = gtfl.logfile
    else:
        gtfl.chkin()
        lfile = gtfl.infile
        if gtfl.qp.search(lfile):
            gtfl.quitout()

    pglgc = ProgLgc()
    pglgc.crtlst(lfile)
    pglgc.rnm()
