#!/usr/bin/env python

import re, argparse
from subprocess import Popen, PIPE

class DF_Usage:
    def __init__(self):
        self.Crit = 11
        self.Fatl = 40
        self.dfcmd = "df -t ext4 -t xfs -h"
        self.sshcmd = ["/usr/bin/ssh", "-o ConnectTimeout=3", "-o StrictHostKeyChecking=no"]
        self.hpatt = re.compile(r'^Filesystem')
        self.blnk = re.compile(r'^$')
        self.head = "\t".join(["Host\t", "FS", "Usage", "Type"])
        self.srvlist = ["ubuntu-vm1", "centos-vm1"]

    def do_ssh(self, srv, cmd):
        self.sshcmd.extend(["%s" % srv, cmd])
        sshresult = Popen(self.sshcmd, stdout=PIPE, stderr= PIPE, universal_newlines=True)
        sshout = sshresult.stdout.readlines()
        ssherr = sshresult.stderr.readlines()
        if ssherr: sshout = ["SSH Failed"]
        del self.sshcmd[-2:]
        return sshout

    def parsedf(self, Host):
        dfout = self.do_ssh(Host, self.dfcmd)
        for dfln in dfout:
            if "SSH Failed" in dfln:
                print("%s\t\t\t%s" % (Host, "SSH Failed"))
                continue
            if self.hpatt.search(dfln) or self.blnk.search(dfln): continue
            fields = dfln.split()
            Pct = fields[4].split('%')[0]
            if int(Pct) > self.Crit and int(Pct) < self.Fatl: fields.append('Critical Alert')
            elif int(Pct) > self.Fatl: fields.append('Fatal Alert')
            else: continue
            lineout = "\t".join([Host, fields[5], fields[4], fields[6]])
            print("%s" % lineout)
        return

    def main(self):
        print("%s" % self.head)
        for H in self.srvlist:
            self.parsedf(H)
        return


if __name__ == "__main__":
    dfusg = DF_Usage()
    dfusg.main()
