#!/usr/bin/env python3

#########################################################################
##                                                                      #
## Parse Iostat output, takes input file as an argument or will prompt  #
## for User input.                                                      #
## Author: Anant Bhat.                                                  #
##                                                                      #
## Please capture all version changes below                             #
## Version 1.0 - Initial creation, Anant, 08/24/2018                    #
#########################################################################

import argparse, re
from subprocess import run

parser = argparse.ArgumentParser(description="Use CyberArk SSH to connect to Linux node")
parser.add_argument("Host", metavar='<host-name>', type=str, help="Specify Hostname to connect")
parser.add_argument("--vaultuser", "-v", type=str, default="abhat_c", help="Specify CyberArk Vault user")
parser.add_argument("--user", "-u", type=str, default="seuseradmin5", help="Specify common assigned user")
args = parser.parse_args()

lcl_accts = ['pythian', 'pythiansa', 'oracle', 'fdadmin', 'wmsadmin', 'sciadmin', 'grid', 'sas']

ecomp = re.compile(r'ecom|crm[ps]|stdev|logistics')
cyb_user = args.vaultuser
comn_user = args.user
Hst = args.Host

### """Check if the host is an ECOM Host"""
if ecomp.search(Hst):
    DOM = "ecomm.web.freshdirect.com"
else:
    DOM = "intranet.biz.freshdirect.com"
CybLB = "cyberarknj.freshdirect.com"
sshcmd = ["/usr/bin/ssh", "-o ConnectTimeout=3"]

### """Check if Common user is a Local account"""
if comn_user in lcl_accts:
    Con_string = str(cyb_user + '@' + comn_user + '@' + Hst + '@' + CybLB)
else:
    Con_string = str(cyb_user + '@' + comn_user + '#' + DOM + '@' + Hst + '@' + CybLB)

sshcmd.extend(["%s" % Con_string])
run(sshcmd)
