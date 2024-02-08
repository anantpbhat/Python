#!/usr/bin/env /usr/bin/python3.6

########################################################################
#                                                                      #
# Parse myhtml Page, takes input file as an argument or will prompt      #
# for User input.                                                      #
# Author: Anant Bhat.                                                  #
#                                                                      #
# Please capture all version changes below                             #
# Version 1.0 - Initial creation, Anant, 02/16/2019                    #
########################################################################

from bs4 import BeautifulSoup
import requests, argparse, os

class Base():
    def __init__(self):
        parser = argparse.ArgumentParser(description="Parse RHEV RESTAPI Output.")
        parser.add_argument("--file", required="true", help="myhtml Filename is required.")
        parser.add_argument("--name", action="store_true", help="Displays Hostname.")
        parser.add_argument("--cpu", action="store_true", help="Displays Host CPU details.")
        parser.add_argument("--ip", action="store_true", help="Displays Host IP.")
        self.args = parser.parse_args()

    def quitout(self):                                      ### Generic Quit method
        exit(code=1)

    def getfile(self):                                      ### Check myhtml file and set a BS file parser object
        if self.args.file and os.path.isfile(self.args.file):
            with open(self.args.file) as rhvhtml:
                self.soupfile = BeautifulSoup(rhvhtml, 'lxml')      ### BS file parser object
        else:
            print("File - {} not found!!!".format(self.args.file))  ### Quit if myhtml file path doesn't exist
            self.quitout()

class BSoup(Base):
    def getname(self):                                      ### Get Hostname
        self.getfile()                                      ### Import myhtml file as soupfile object
        print("")
        name = self.soupfile.find('name')
        print("HOSTNAME:\t{}".format(name.text))

    def getcpu(self):                                       ### Get CPU Details
        self.getfile()                                      ### Import myhtml file as soupfile object
        print("")
        CPU = self.soupfile.find('cpu')                     ### Section <cpu> in myhtml file is assigned to CPU
        cpu_cores = CPU.topology["cores"]                   ### Topology has name/value pair attributes, so dict is used
        print("CPU:\tCores - {}".format(cpu_cores))
        cpu_name_speed = CPU.find('name').text.split("@")   ### "name" cannot be extracted, hence find is used
        print("CPU:\tType - {}".format(cpu_name_speed[0]))  ### CPU Type from 1st field of name_speed array
        print("CPU:\tSpeed - {}".format(cpu_name_speed[1])) ### CPU Speed from 2nd field

    def getip(self):                                        ### Get IP Address
        self.getfile()                                      ### Import myhtml file as soupfile object
        print("")
        IP = self.soupfile.find('address')                  ### Section <address> in myhtml file is now IP
        print("IP Addr:\t{}".format(IP.text))

### Main Program starts here ###
if __name__ == "__main__":
    bs = BSoup()
    if bs.args.name:
        bs.getname()

    if bs.args.cpu:
        bs.getcpu()

    if bs.args.ip:
        bs.getip()
