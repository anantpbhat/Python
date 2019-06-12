#!/usr/bin/env python

import argparse, re
from subprocess import Popen, PIPE

class RNMNIC:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Provides old-style simple and persistent naming to physical / wireless network interfaces")
        self.args = parser.parse_args()

    def getnicinfo(self):
        patt = re.compile(r'(^Bus info)|(^===)')
        mpatt = re.compile(r'(pci)|(usb)')
        (i, j, k) = (0, 0, 0)
        nicinfo = []
        cmd = ("/usr/bin/lshw", "-businfo", "-C", "network")
        with Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True) as lshw:
            for line in lshw.stdout.readlines():
                if patt.search(line) or line == "": continue
                if mpatt.search(line):
                    nicinfo.append({})
                    lineary = line.split()
                    nicinfo[i]["name"] = lineary[1]
                    if "Wireless" in line:
                        nicinfo[i]["newname"] = "wlan" + str(k)
                        nicinfo[i]["type"] = "Wireless"
                        k += 1
                    else:
                        nicinfo[i]["newname"] = "eth" + str(j)
                        nicinfo[i]["type"] = "Physical"
                        j += 1
                    ipcmd = ["/sbin/ip", "addr", "show"]
                    ipcmd.append(nicinfo[i]["name"])
                    with Popen(ipcmd, stdout=PIPE, stderr=PIPE, universal_newlines=True) as ip_cmd:
                        for ipline in ip_cmd.stdout.readlines():
                            if "link/ether " in ipline:
                                nicinfo[i]["ether"] = ipline.split()[1]
                                break
                            continue
                    i += 1
        return nicinfo

    def main(self):
        nics = self.getnicinfo()
        for itm in nics:
            print("NIC %s with ethernet address: %s will become %s" % (itm["name"], itm["ether"], itm["newname"]))
        return


if __name__ == "__main__":
    rnmnic = RNMNIC()
    rnmnic.main()
