#!/usr/bin/env /usr/bin/python3.5

#########################################################################
##                                                                      #
## Parse Iostat output, takes input file as an argument or will prompt  #
## for User input.                                                      #
## Author: Anant Bhat.                                                  #
##                                                                      #
## Please capture all version changes below                             #
## Version 1.0 - Initial creation, Anant, 08/24/2018                    #
#########################################################################

import argparse
import re
import datetime

parser = argparse.ArgumentParser(description="Parse IOSTAT Data with provided input file.")
parser.add_argument("-i", "--infile", metavar="", help="Specify IOSTAT Data file path")
args = parser.parse_args()

qp = re.compile(r'^q$|^quit$', re.I)
dtp = re.compile(r'/2018 [0-9:]+ [AP]M$')

def getdt():
        dttm = datetime.datetime.now()
        dt = (str(dttm.year) +  str(dttm.month) + str(dttm.day))
        return dt

def getinput():
        IN1 = input("Enter IOSTAT Data file path or (q|Q) to quit: ")
        if qp.search(IN1):
                print("Exiting at users request...!")
                exit(0)
        else:
                return IN1

if args.infile:
        IOFILE = args.infile
else:
        IOFILE = getinput()

DT = getdt()
wfile = "iostat_" + DT + ".csv"
fstline = "Date, Time, %User CPU, %System CPU, %IOWait, %CPU Idle, R/sec, W/sec, Avg-Q, Avg-W, SvcTm, %Util"
jo = ",\t"
iowf = open(wfile, 'w')
iowf.write(fstline + "\n")
with open(IOFILE, 'r') as iorf:
        for line in iorf:
                if dtp.search(line):
                        dtary = line.split()
                        iowf.write(dtary[0] + ", " + dtary[1] + " " + dtary[2] + jo)
                if line.startswith("avg-cpu:"):
                        cpuary = next(iorf).split()     ### Get the next line after avg-cpu and split it to get a list
                        iowf.write(cpuary[0] + jo + cpuary[2] + jo + cpuary[3] + jo + cpuary[5] + jo)
                if line.startswith("sda"):
                        dskary = line.split()
                        iowf.write(dskary[3] + jo + dskary[4] + jo + dskary[8] + jo + dskary[9] + jo + dskary[12] + jo + dskary[13] + "\n")
iowf.close