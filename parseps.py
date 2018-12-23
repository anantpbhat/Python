#!/usr/bin/env python3.6

########################################################################
#                                                                      #
# Parse Unix PS output, takes input file as an argument or will prompt #
# for User input.                                                      #
# Author: Anant Bhat.                                                  #
#                                                                      #
# Please capture all version changes below                             #
# Version 1.0 - Initial creation, Anant, 12/24/2018                    #
########################################################################

import argparse, re
from datetime import datetime


class Argsnregx():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Parse Unix PS output from a file.")
        self.parser.add_argument("-i", "--infile", metavar="", help="Specify PS Data file path")
        self.parser.add_argument("-p", "--pid", metavar="", help="Specify PID to monitor")
        self.parser.add_argument("-u", "--user", metavar="", help="Specify Username to monitor")
        self.args = self.parser.parse_args()
        # First Header line output in CSV File
        self.far = ["Date", "Time", "PID", "User", "%CPU", "%Mem", "Threads", "Resident Mem", "Virtual Mem", "Command"]
        self.cur_yr = "2018"                                    # Specify Current year here
        self.qp = re.compile(r'^q$|^quit$', re.I)               # Case insensitive search pattern for quit
        self.dtp = re.compile(r'E[SD]T ' + self.cur_yr + r'$')  # Search for ending with EST/EDT & current year


class GetInput(Argsnregx):
    def quitout(self, qstr):
        self.qstr = qstr
        if self.qp.search(self.qstr):
            print("Quiting at users request...")
            exit(0)

    def getdt(self):                                            # Get Date & Time in correct format
        self.dttm = datetime.now()
        self.dt = "-".join([str(self.dttm.year), str(self.dttm.month), str(self.dttm.day)])
        self.tm = ":".join([str(self.dttm.hour), str(self.dttm.minute), str(self.dttm.second)])

    def chkin(self):                                            # Get all the Inputs
        if not self.args.infile:
            self.infile = input("Enter Filename with PS output or (q|Q) to quit: ").strip()
            self.quitout(self.infile)
        else:
            self.infile = self.args.infile

        if not self.args.pid:
            self.pid = input("Enter PID for the process to be monitored or (q}Q) to quit: ").strip()
            self.quitout(self.pid)
        else:
            self.pid = self.args.pid

        if not self.args.user:
            self.user = input("Enter Username of the process or (q|Q) to quit: ").strip()
            self.quitout(self.user)
        else:
            self.user = self.args.user


if __name__ == "__main__":
    gtinp = GetInput()
    gtinp.getdt()
    gtinp.chkin()
    pup = re.compile(r'\b' + gtinp.pid + " " + gtinp.user + r'\b')  # Search word boundaries with variable in pattern
    wfile = "/home/abhat/psout_" + gtinp.dt + ".csv"
    jo = ",\t"
    fstline = jo.join(gtinp.far)
    with open(gtinp.infile) as psrf, open(wfile, 'w') as pswf:
        pswf.write(fstline + "\n")
        for psline in psrf:
            if gtinp.dtp.search(psline):                            # Date line ending with EST/EDT & current year
                dtary = psline.split()
                strng1 = dtary[1] + " " + dtary[2]
                pswf.write(jo.join([strng1, dtary[3]]) + jo)
            elif pup.search(psline):                                # Search for PID & Username in PS output
                ary1 = psline.split()
                if len(ary1) > 10:
                    del ary1[10:]
                pswf.write(jo.join(ary1) + "\n")
            else:
                pass
