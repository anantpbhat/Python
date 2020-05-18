#!/usr/bin/env python
import re
from subprocess import Popen, PIPE, check_output

#def getprice(x):
#    if x in cmdty:
#        print("Price for item '{}' is: {} USD".format(x, cmdty[x]), "\n")
#    else:
#        print("{} is not a valid item".format(x), "\n")

#cmdty = {"Soccer Ball": 9, "Rice": 3, "Python Book": 30, "Apples": 2, "Printer": 150}
#qp = re.compile(r'^(q|quit)$', re.I)

#while True:
#    ui = input("Enter a Commodity Name: ")
#    if qp.search(ui):
#        print("Quiting at users request...")
#        break
#    else:
#        getprice(ui.title())
#        continue
#exit(0)

DF = "df -t ext4 -t xfs -h"
SSH = ["/usr/bin/ssh", "-o ConnectTimeout=1", "-o StrictHostKeyChecking=yes"]
srvlist = ["ubuntu-vm1", "centos-vm1"]

def do_ssh(Host, cmd):
    SSH.extend(["%s" % Host,cmd])
    sshcmd = ["/usr/bin/ssh", "-o ConnectTimeout=10", "-o StrictHostKeyChecking=yes", "%s" % Host, cmd]
    result = Popen(SSH, stdout=PIPE, stderr=PIPE)
    sshout = result.stdout.readlines()
    del SSH[-1]
    return sshout

for H in srvlist:
    Out = do_ssh(H, DF)
    print(Out)