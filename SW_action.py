#!/usr/bin/env python3

#########################################################################
##                                                                      #
## ADD newly built Server in SolarWinds.                                #
## Author: Anant Bhat.                                                  #
##                                                                      #
## Please capture all version changes below                             #
## Version 1.0 - Initial creation, Anant, 01/10/2021                    #
#########################################################################

import re, argparse, requests, imp
from ansible.module_utils.basic import AnsibleModule

class SW_Base:
        def __init__(self):
                fields = {
                        "nodename":     {"required": True, "type": "str"},
                        "ip_address":   {"required": True, "type": "str"},
                        "device_func":  {"default": "", "type": "str"},
                        "action":       {"required": True, "type": "str"},
                }
                module = AnsibleModule(argument_spec=fields)
                """Check if module exists before importing"""
                try:
                        imp.find_module('orionsdk')
                        from orionsdk import SwisClient
                except ImportError:
                        module.fail_json(msg="'orionsdk' not found.  Is the module installed?")
                        module.exit_json(changed=True)
                SW_Server = 'solarwinds.nj01'
                SW_User = 'svc-solaradmin-test'
                SW_Passwd = 'SOLAR_5689!'
                self.swis = SwisClient(SW_Server, SW_User, SW_Passwd)
                self.node = module.params['nodename']
                self.ipaddr = module.params['ip_address']
                self.action = module.params['action']
                self.devfunc = module.params['device_func']
                self.module = module
                requests.packages.urllib3.disable_warnings()


class SW_Query():
        def __init__(self):
                self.base = SW_Base()
                out = self.base.swis.query("SELECT n.Uri FROM Orion.Nodes n WHERE n.Caption = '%s'" % self.base.node)
                self.uri = out['results'][0]['Uri']
                custprops = (("%s" + "/CustomProperties") % self.uri)
                self.props = self.base.swis.read('%s' % self.uri)
                self.custprops = self.base.swis.read('%s' % custprops)
                self.log = []
                self.result = {}

        def printvals(self):
                self.log.append("SW Node URI: %s" % self.uri)
                self.log.append("SW Node Properties: %s" % self.props)
                self.log.append("SW Node Custom Properties: %s" % self.custprops)
                self.result['changed'] = False
                self.result['msg'] = self.log
                return

        def main(self):
                self.printvals()
                self.base.module.exit_json(**self.result)
                return


class SW_AddNode():
        def __init__(self):
                self.base = SW_Base()
                self.nprops = {
                        'IPAddress': self.base.ipaddr,
                        'EngineID': 6,
                        'ObjectSubType': 'SNMP',
                        'SNMPVersion': 3,
                        'Caption': self.base.node,
                        'SNMPV3AuthKey': 'S3MS321sw',
                        'SNMPv3AuthKeyIsPwd': True,
                        'SNMPv3AuthMethod': 'SHA1',
                        'SNMPv3PrivKey': 'S4MS321sw',
                        'SNMPv3PrivKeyIsPwd': True,
                        'SNMPv3PrivMethod': 'AES128',
                        'SNMPV3Username': 'snmpadmin'
                }
                self.log = []
                self.result = {}

        def addnode(self):
                results = self.base.swis.create('Orion.Nodes', **self.nprops)
                nodeid = re.search('(\d+)$', results).group(0)
                return (results, nodeid)

        def initpollers(self, nid):
                set_pollers = {
                'N.Status.ICMP.Native': True,
                'N.Status.SNMP.Native': False,
                'N.ResponseTime.ICMP.Native': True,
                'N.ResponseTime.SNMP.Native': False,
                'N.Details.SNMP.Generic': True,
                'N.Uptime.SNMP.Generic': True,
                'N.Cpu.SNMP.HrProcessorLoad': True,
                'N.Memory.SNMP.NetSnmpReal': True,
                'N.AssetInventory.Snmp.Generic': True,
                'N.Status.SNMP.Native': False,
                'N.ResponseTime.SNMP.Native': False,
                'N.Topology_Layer3.SNMP.ipNetToMedia': False,
                'N.Routing.SNMP.Ipv4CidrRoutingTable': False
                }
                pollers = []
                for K in set_pollers:
                        pollers.append(
                        {
                        'PollerType': K,
                        'NetObject': 'N:' + nid,
                        'NetObjectType': 'N',
                        'NetObjectID': nid,
                        'Enabled': set_pollers[K]
                        }
                )
                return pollers

        def popcust(self):
                hst = self.base.node
                dfunc = self.base.devfunc
                ctvals = {}
                njsp = re.compile(r'^nj01')
                azsp = re.compile(r'^az01')
                hrysp = re.compile(r'^hry')
                if hst.startswith('nj01'): ctvals["Site"] = "Nj01 - Telx Co-Lo"
                if hst.startswith('az01'): ctvals["Site"] = "Azure Cloud"
                if hst.startswith('hry'): ctvals["Site"] = "HRY - Bronx"
                if hst[4] == 'l':
                        ctvals["OS"] = "Linux"
                        ctvals["DeviceLoc"] = "Linux Servers"
                        ctvals["DeviceType"] = "Linux Servers"
                if hst[4] == 'w':
                        ctvals["OS"] = "Windows"
                        ctvals["DeviceLoc"] = ""
                        ctvals["DeviceType"] = "Servers"
                """Assign Device function from input value provided by module else extract from hostname"""
                if dfunc: ctvals['DevFunc'] = dfunc
                elif hst[5:8] == 'pma' or hst[5:10] == 'pmanh': ctvals['DevFunc'] = "PRD Manhattan Associates"
                elif hst[5:8] == 'dma' or hst[5:10] == 'dmanh': ctvals['DevFunc'] = "DEV Manhattan Associates"
                elif hst[5:10] == 'dtdal' or hst[5:10] == 'ptdal': ctvals['DevFunc'] = "Tidal Servers"
                elif hst[5:10] == 'ddwrh' or hst[5:10] == 'pdwrh': ctvals['DevFunc'] = "Data Warehouse"
                elif hst[5:13] == 'dcorejbx': ctvals['DevFunc'] = "Misc Linux Servers"
                else: ctvals['DevFunc'] = ""    ### Don't assign if none matches
                return ctvals

        def addcust(self, vals, inpt):
                custprops = {
                'AssetTag': "",
                'Building': "",
                'DeviceFunction': vals['DevFunc'],
                'DeviceLocation': vals['DeviceLoc'],
                'DeviceType': vals['DeviceType'],
                'EsxiLocation': "None",
                'Maintanance_mode': False,
                'OS': vals['OS'],
                'PDIntegrationKey': "",
                'Site': vals['Site']
                }
                for K, V in custprops.items():
                        self.base.swis.update(inpt + "/CustomProperties", **{K: V})
                        self.log.append("Custom property '%s' added with value - %s" % (K, V))
                return

        def main(self):
                (URL, NID) = self.addnode()
                plist = self.initpollers(NID)
                for P in plist:
                        msg = ("Adding poller type: %s with status %s ... " % (P['PollerType'], P['Enabled']))
                        resp = self.base.swis.create('Orion.Pollers', **P)
                        self.log.append(msg + " DONE!")
###             self.base.swis.invoke('Orion.Nodes', 'PollNow', 'N' + NID)
                custvals = self.popcust()
                self.addcust(custvals, URL)
                self.result['changed'] = True
                self.result['msg'] = self.log
                self.base.module.exit_json(**self.result)
                return


if __name__ == "__main__":
        SWB = SW_Base()
        if SWB.action == "query":
                SWQ = SW_Query()
                SWQ.main()
        elif SWB.action == "add":
                SWAN = SW_AddNode()
                SWAN.main()
        else:
                pass
