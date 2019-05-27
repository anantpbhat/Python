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
        parser.add_argument("-o", "--output", metavar="", help="Specify a filename prefix to output. Optional")
        self.args = parser.parse_args()

    def getdatetime(self):
        DT = str(datetime.now()).split(".")
        dttm = DT[0].split()
        return (dttm[0], dttm[1])

    def getfilename(self):
        (arg1, arg2) = self.getdatetime()
        if self.args.output == "stdout" or not self.args.output:
            return "stdout"
        else:
            return str("Out/%s_%s_%s" % (self.args.output, arg1, arg2))

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

    def writeout(self, arg1, arg2, lst1, file1):
        SET1 = str("DATE: %s %s" % (arg1, arg2)) + "\t" + str("PID: %d" % lst1[3])
        SET2 = str("%s" % lst1[0]) + "\n" + str("%s" % lst1[1]) + "\n" + str("%s" % lst1[2]) + "\n"
        if file1 == "stdout":
            print(SET1)
            print(SET2)
        else:
            with open(file1, 'a') as f:
                f.write(SET1 + "\n")
                f.write(SET2 + "\n")
        return

    def main(self):
        intvl = int(self.args.interval)
        cnt = int(self.args.count)
        outfile = self.getfilename()
        while cnt > 0:
            (dt, tm) = self.getdatetime()
            memstat = self.getmemstat()
            self.writeout(dt, tm, memstat, outfile)
            cnt -= 1
            if cnt != 0:
                sleep(intvl)
        return


if __name__ == "__main__":
    mem = MEMSTAT()
    mem.main()
