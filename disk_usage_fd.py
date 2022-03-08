#!/usr/bin/env python3

#########################################################################
##                                                                      #
## Report Disk Filesystem Usage for Servers.                            #
## Author: Anant Bhat.                                                  #
##                                                                      #
## Please capture all version changes below                             #
## Version 1.0 - Initial creation, Anant, 05/25/2020                    #
##                                                                      #
#########################################################################

import re, argparse
from subprocess import Popen, PIPE

class DF_Usage:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Reports Disk Usage for specified Manhattan Servers")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--qa2", "-Q", action="store_true", help="Report usage for qa2 servers.")
        group.add_argument("--prod", "-P", action="store_true", help="Report usage for Prod servers.")
        group.add_argument("--all", "-A", action="store_true", help="Report usage for All Manhattan servers.")
        parser.add_argument("--email", "-E", type=str, default="abhat@freshdirect.com", help="Provide Email address to report on.")
        self.args = parser.parse_args()
        self.Crit = 55
        self.Fatl = 70
        self.qalist = ["nj01ldmawm04", "nj01ldmawm05", "nj01ldmawmrf04", "nj01ldmawmrf05", "nj01ldmamif04", "nj01ldmamif05", "NoHost"]
        self.prodlist = ["nj01lpmawm02", "nj01lpmawm02", "nj01lpmawmrf01", "nj01lpmawmrf02", "nj01lpmamif01", "nj01lpmamif02"]
        self.TO = self.args.email
        self.FROM = 'Anant Bhat <abhat@freshdirect.com>'
        self.SUB = "Disk Usage for Manhattan Servers - Over 75%"
        self.dfcmd = "df -t ext4 -t xfs -h"
        self.mailcmd = ["/usr/sbin/sendmail", "-t"]
        self.hpatt = re.compile(r'^Filesystem')
        self.blnk = re.compile(r'^$')
        self.bnrp = re.compile(r'^#.*#$')
        self.listout = []

    def get_srvs(self):
        srvs = []
        if self.args.prod: srvs = self.prodlist
        elif self.args.qa2: srvs = self.qalist
        elif self.args.all:
            srvs.extend(self.qalist)
            srvs.extend(self.prodlist)
        else:
            print("No Server arguments given - Atleast one is needed!!! Exiting...")
            exit(1)
        return srvs

    def do_ssh(self, srv, cmd):
        Err = []
        sshcmd = ["ssh", "-o ConnectTimeout=3", "-o StrictHostKeyChecking=no"]
        sshcmd.extend(["%s" % srv, cmd])
        sshresult = Popen(sshcmd, stdout=PIPE, stderr= PIPE, universal_newlines=True)
        sshout = sshresult.stdout.readlines()
        ssherr = sshresult.stderr.readlines()
        for errln in ssherr:
            if not self.bnrp.search(errln): Err.append(errln)
        if Err: sshout = ["SSH Failed"]
        return sshout

    def parsedf(self, Host, cnt):
        dfout = self.do_ssh(Host, self.dfcmd)
        self.listout.append({})
        for dfln in dfout:
            dfln = dfln.strip()
            if "SSH Failed" in dfln:
                self.listout[cnt]["Name"] = str("<td>" + Host + "</td>")
                self.listout[cnt]["FS"] = "<td> NA </td>"
                self.listout[cnt]["Usg"] = "<td> NA </td>"
                self.listout[cnt]["Alert"] = '<td><strong style="color: blue;"> SSH Failed </strong></td>'
                continue
            if self.hpatt.search(dfln) or self.blnk.search(dfln): continue
            fields = dfln.split()
            Pct = fields[4].split('%')[0]
            if int(Pct) > self.Crit and int(Pct) < self.Fatl: fields.append('<strong style="color: orange;">Critical Alert</strong>')
            elif int(Pct) > self.Fatl: fields.append('<strong style="color: red;">Fatal Alert</strong>')
            else: continue
            self.listout[cnt]["Name"] = str("<td>" + Host + "</td>")
            self.listout[cnt]["FS"] = str("<td>" + fields[5] + "</td>")
            self.listout[cnt]["Usg"] = str("<td>" + fields[4] + "</td>")
            self.listout[cnt]["Alert"] = str("<td>" + fields[6] + "</td>")
        return

    def printout(self):
        HeaderP1 = """
<html>
  <head><h1>"""
        HeaderP2 = """</h1></head>
  <body>
    <table>"""
        Header = str(HeaderP1 + self.SUB + HeaderP2)
        RowStart = '      <tr>'
        RowEnd = '</tr>'
        Head = "<th> Host </th><th> FS </th><th> Usage </th><th> Type </th>"
        HeadRow = str(RowStart + Head + RowEnd)
        Footer = """    </table>
  </body>
</html>"""
        MIME = """Mime-Version: 1.0
Content-type: text/html; charset=\"iso-8859-1\"
"""
        MetaData = str("From: " + self.FROM + "\n" + "To: " + self.TO + "\n" + "Subject: " + self.SUB + "\n" + MIME)
        mlines = []
        for entry in self.listout:
            if not entry: continue
            line = "  ".join([entry["Name"], entry["FS"], entry["Usg"], entry["Alert"]])
            mlines.append(str(RowStart + line + RowEnd))
        Body = "\n".join(mlines)
        MailString = str(MetaData + Header + HeadRow + "\n" + Body + Footer + "\n")
        with Popen(self.mailcmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True) as smail:
            (mout, merr) = smail.communicate(input=MailString)
        if merr: print("Error sending email, check localhost postfix config!")
        return

    def main(self):
        i = 0
        srvlist = self.get_srvs()
        for H in srvlist:
            self.parsedf(H, i)
            i += 1
        self.printout()
        return


if __name__ == "__main__":
    dfusg = DF_Usage()
    dfusg.main()
