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
cpup = re.compile(r'^avg-cpu:')
sdap = re.compile(r'^sda\s+')

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
iowf = open(wfile, 'w')
iowf.write(fstline + "\n")
with open(IOFILE, 'r') as iorf:
        for line in iorf:
                if dtp.search(line):
                        dtary = line.split()
                        iowf.write(dtary[0] + ", " + dtary[1] + " " + dtary[2] + ",\t")
                if cpup.search(line):
                        cpuary = next(iorf).split()     ### Get the next line after avg-cpu and split it to get a list
                        iowf.write(cpuary[0] + ",\t" + cpuary[2] + ",\t" + cpuary[3] + ",\t" + cpuary[5] + ",\t")
                if sdap.search(line):
                        dskary = line.split()
                        iowf.write(dskary[3] + ",\t" + dskary[4] + ",\t" + dskary[8] + ",\t" + dskary[9] + ",\t" + dskary[12] + ",\t" + dskary[13] + "\n")
iowf.close