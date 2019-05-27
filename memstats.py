#!/usr/bin/env python

import argparse
from subprocess import Popen, PIPE, check_output
from datetime import datetime
from time import sleep

class MEMSTAT:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Display Memstats with timestamps. Interval & Count args required")
        parser.add_argument("-i", "--interval", required=True, metavar="", help="Interval is required, specify in secs")
        parser.add_argument("-c", "--count", required=True, metavar="", help="Count is required, specify a number")
        self.args = parser.parse_args()

    def getdatetime(self):
        DT = str(datetime.now()).split(".")
        return DT[0]

    def getmemstat(self):
        memstatout = []
        header = ("Resource", "Total(GB)", "Used(GB)", "Free(GB)")
        headerln = "\t".join(header)
        memstatout.append(headerln)
        memcmd = ("/usr/bin/free", "-m")
        with Popen(memcmd, stdout=PIPE, stderr=PIPE, universal_newlines=True) as memproc:
            for line in memproc.stdout.readlines():
                if line.startswith("Mem:"):
                    memline = line.split()
                    tmem = float(memline[1]) / 1024.0
                    umem = float(memline[2]) / 1024.0
                    fmem = float(int(memline[3]) + int(memline[4]) + int(memline[6])) / 1024.0
                    memout = ("Memory", "", "%.2f" % tmem, "", "%.2f" % umem, "", "%.2f" % fmem)
                    memoutln = "\t".join(memout)
                    memstatout.append(memoutln)
                if line.startswith("Swap:"):
                    swpline = line.split()
                    tswp = float(swpline[1]) / 1024.0
                    uswp = float(swpline[2]) / 1024.0
                    fswp = float(swpline[3]) / 1024.0
                    swpout = ("Swap", "", "%.2f" % tswp, "", "%.2f" % uswp, "", "%.2f" % fswp)
                    swpoutln = "\t".join(swpout)
                    memstatout.append(swpoutln)
            memstatout.append(memproc.pid)
        return memstatout

    def main(self):
        intvl = int(self.args.interval)
        cnt = int(self.args.count)
        while cnt > 0:
            DATE = self.getdatetime()
            memstat = self.getmemstat()
            print("DATE: %s" % DATE, "\t", "PID: %d" % memstat[3])
            print("%s" % memstat[0], "\n", "%s" % memstat[1], "\n", "%s" % memstat[2], "\n")
            cnt -= 1
            if cnt != 0:
                sleep(intvl)
        return


if __name__ == "__main__":
    mem = MEMSTAT()
    mem.main()
