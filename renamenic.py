#!/usr/bin/env python

import argparse, re, fileinput
from subprocess import Popen, PIPE
from os import path, mkdir, rename
from datetime import datetime

class RNMNIC:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Provides old-style simple and persistent naming to physical / wireless network interfaces")
        parser.add_argument("--info", action="store_true", help="print NIC Info")
        parser.add_argument("--update", action="store_true", help="Generate persistent Net rules file")
        self.args = parser.parse_args()

    def getdttm(self):
        dttm_lst = str(datetime.now()).split()
        dttm = "_".join((dttm_lst[0], dttm_lst[1].split('.')[0]))
        return dttm

    def chkuser(self):
        with Popen(["id"], stdout=PIPE, universal_newlines=True) as ID:
            for idline in ID.stdout.readlines():
                UID = int(idline.split('(')[0].split('=')[1])
                if UID != 0:
                    print("Only root is allowed to perform this function, Quiting...!")
                    exit(1)
        return

    def getnicinfo(self):
        patt = re.compile(r'(^Bus info)|(^===)')
        mpatt = re.compile(r'(pci)|(usb)')
        (i, j, k) = (0, 0, 0)
        nicinfo = []
        netrules1 = 'SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="'
        netrules2 = '", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="p*", NAME="'
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
                    nicinfo[i]["ip"] = "None"
                    with Popen(ipcmd, stdout=PIPE, stderr=PIPE, universal_newlines=True) as ip_cmd:
                        for ipline in ip_cmd.stdout.readlines():
                            if "link/ether " in ipline:
                                nicinfo[i]["ether"] = ipline.split()[1]
                            elif "inet " in ipline:
                                nicinfo[i]["ip"] = ipline.split()[1]
                            continue
                    nicinfo[i]["netrules"] = netrules1 + nicinfo[i]["ether"] + netrules2 + nicinfo[i]["newname"] + '"'
                    i += 1
        return nicinfo

    def create_netrules(self, niclst):
        self.chkuser()
        UDEV_DIR = "/etc/udev/rules.d/"
        UDEV_File = "70-persistent-net.rules"
        dtntm = self.getdttm()
        if not path.exists(UDEV_DIR + "archive"):
           mkdir(UDEV_DIR + "archive")
        if path.exists(UDEV_DIR + UDEV_File):
           rename(UDEV_DIR + UDEV_File, UDEV_DIR + "archive/" + UDEV_File + "." + dtntm)
        with open(UDEV_DIR + UDEV_File, 'w') as netrulefile:
            for inf in niclst:
                netrulefile.write(inf["netrules"] + "\n")
        return

    def update_grubnet(self):
        self.chkuser()
        grbpatt = re.compile(r'^GRUB_CMDLINE_LINUX=""')
        DF_DIR = "/etc/default/"
        dtntm = self.getdttm()
        if not path.exists(DF_DIR + "archive"):
            mkdir(DF_DIR + "archive")
        for grbln in fileinput.input(DF_DIR + "grub", inplace=True, backup=".bak"):
            if grbpatt.search(grbln):
                grbln = 'GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"'
            print(grbln.rstrip())
        rename(DF_DIR + "grub.bak", DF_DIR + "archive/grub" + "." + dtntm)
        Popen(["/usr/sbin/update-grub"], stdout=PIPE, universal_newlines=True)

    def main(self):
        nics = self.getnicinfo()
        if self.args.info:
            for itm in nics:
                print("NIC %s with ethernet address: %s and IP: %s will become %s" % (itm["name"], itm["ether"], itm["ip"], itm["newname"]))
                print("So the Netrules string is - %s" % itm["netrules"])
                print()
        elif self.args.update:
            self.create_netrules(nics)
            self.update_grubnet()
        else:
            print("At least One argument is required.")
            print("Usage: renamenic.py --info | --update")
        return


if __name__ == "__main__":
    rnmnic = RNMNIC()
    rnmnic.main()
