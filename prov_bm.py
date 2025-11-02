#!/usr/bin/python

import re, requests, json, time
from ucsmsdk.ucshandle import UcsHandle
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.sshconn import SSHConn

class BaseCl():
  """Base class to define all common base vars and input args"""
  def __init__(self):
    module_args = dict (
      serveros = dict(type = 'str, required = True, choices = ['rhel8', 'rhel9']),
      serverenv = dict(type = 'str, required = True, choices = ['Lab', 'Test', 'QA', 'Prod']),
      servername = dict(type= 'str', required = True),
      servermgmt = dict(type= 'str', required = True),
      mgmtuser = dict(type= 'str', required = True),
      mgmtusrp = dict(type= 'str', required = True),
      serverip = dict(type= 'str', required = True),
      servernetmask = dict(type= 'str', required = True),
      servergateway = dict(type= 'str', required = True),
      servervlan = dict(type= 'str', required = True),
      cisco = dict(type = 'dict',
                required = False,
                options = dict(
                    chassis = dict(type= 'str', required = True),
                    blade = dict(type= 'str', required = True),
                    model = dict(type= 'str', required = True, choices = ['m5', 'm7'])
                )
              ),
        dell = dict(type = 'dict',
                    required = False,
                    options = dict(
                        model = dict(type = 'str', required = True, choices = ['r750', 'r760_emr', 'r760_spr'])
                    )
                )
        )
        self.module = AnsibleModule(
            argument_spec = module_args,
            supports_check_mode = True
        )
        self.log = []
        self.results = {}


class MainProg(BaseCl):
  """Main program class"""
  def __init__(self):
    super().__init__()
    if self.module.params['cisco']:
      self.chassis = self.module.params['cisco']['chassis']
      self.blade = self.module.params['cisco']['blade']
      self.hwmdl = self.module.params['cisco']['model']
      self.domusr = f"ucs-AMS\\{self.module.params['mgmtuser']}"
    elif self.module.params['dell']:
      self.domusr = f"{self.module.params['mgmtuser']}@ams.bnymellon.net"
      if "r750" in self.module.params['dell']['model']:
        self.nicslt = "1-1-1"
        self.nicpri = "ens1f0np0"
        self.infsec = "ens3f0np0"
        self.hwmdl = "r750"
      if "r760_emr" in self.module.params['dell']['model']:
        self.nicslt = "1-1-1"
        self.nicpri = "ens1f0np0"
        self.infsec = "ens7f0np0"
        self.hwmdl = "r760"
      if "r760_spr" in self.module.params['dell']['model']:
        self.nicslt = "3-1-1"
        self.nicpri = "ens3f0np0"
        self.infsec = "ens4f0np0"
        self.hwmdl = "r760"
      else:
        pass
    else:
      pass

  def getenvvars(self):
    """Function to get all Variables per ENV"""
    satvars = {}
    if self.module.params['serverenv'].lower() == 'lab':
      satvars['sat_host'] = 'satlabserver.abc.net'
      satvars['sat_api_url'] = f"https://{satvars['sat_host']}/api/hosts"
      satvars['sat_org_id'] = '1'
      satvars['sat_loc_id'] = '2'
      satvars['pxe_subnet_id'] = '1'
      satvars['lab_subnet_id'] = '2'
      satvars['sat_hgid'] = {
        'rhel9_dell_r760': '2',
        'rhel8_dell_r760': '3',
        'rhel9_cisco_m5': '4',
        'rhel9_cisco_m7': '4',
        'rhel8_cisco_m5': '5',
        'rhel8_cisco_m7': '5',
        'rhel9_dell_r750': '6',
        'rhel8_dell_r750': '7'
      }
    return satvars

  def getucsmac(self):
    """Function to query UCSM and extract primary NIC MAC"""
    nic_adapter = "1"
    eth_if = "1"
    DN = f"sys/chassis-{self.chassis}/blade-{self.blade}/adaptor-{nic_adaptor}/host-eth-{eth_if}"
    ucsm_handle = UcsHandle(self.module.params['servermgmt'], self.domusr, self.module.params['mgmtusrp'])
    ucsm_handle.login()
    eth_if_info = ucsm_handle.query_dn(DN)
    if eth_if_info:
      mac_addr = eth_if_info.mac
    else:
      mac_addr = None
      self.log.append(f"UCSM connection to - {self.module.params['servermgmt']} failed!!")
    ucsm_handle.logout()
    inf_pri = "eno5"
    inf_sec = "eno6"
    return mac_addr, inf_pri, inf_sec

  def getdellmac(self):
    """Function to query Dell iDRAC and extract primy NIC MAC"""
    Ssh = SSHConn()
    dellcmd = f"racadm hwinventory NIC.Slot.{self.nicslt}"
    dellp = re.compile(r'^Permanent MAC Address:')
    sshresult = Ssh.do_ssh(self.module.params['servermgmt'], dellcmd, self.domusr, self.module.params['mgmtusrp'])
    if "SSH failed" in sshresult:
      mac_addr = None
      self.log.append(f"SSH failed connecting to - {self.module.params['servermgmt']}: {sshresult}")
    else:
      for sshline in sshresult.splitlines():
        if dellp.search(sshline):
          mac_arry = sshline.split()
          mac_addr = mac_arry[3]
    inf_pri = self.infpri
    inf_sec = self.infsec
    return mac_addr, inf_pri, inf_sec

  def setuphost(self, arg1, arg2, arg3, arg4):
    """Function to setup Host entry on respective Satellite Server"""
    OS = self.module.params['serveros'].lower()
    HW = arg1
    MDL = self.hwmdl
    ether = arg2
    if_pri = arg3
    if_sec = arg4
    hostvars = self.getenvvars()
    payload = {
      "host": {
        "name": self.module.params['servername'].lower(),
        "domain_id": "1",
        "hostgroup_id": hostvars['sat_hgid'][f"{OS}_{HW}_{MDL}"],
        "organization_id": hostvars['sat_org_id'],
        "location_id": hostvars['sat_loc_id'],
        "architecture_id": '1',
        "pxe_loader": "Grub2 UEFI SecureBoot",
        "provision_method": "build",
        "managed": True,
        "build": True,
        "enabled": True,
        "interface_attributes": [
          {
            "mac": ether,
            "type": "interface",
            "ip": "",
            "subnet_id": hostvars['pxe_subnet_id'],
            "domain_id": "1",
            "identifier": if_pri,
            "primary": True,
            "managed": True,
            "provision": True
          }
        ],
        "host_parameters_attributes": [
          {
            "name": "bondslaves",
            "value": f"{if_pri},{if_sec}"
          },
          {
            "name": "ip_addr",
            "value": self.module.params['serverip']
          },
          {
            "name": "ip_gateway",
            "value": self.module.params['servergateway']
          },
          {
            "name": "ip_netmask",
            "value": self.module.params['servernetmask']
          },
          {
            "name": "vlan_id",
            "value": self.module.params['servervlan']
          }
        ]
      }
    }
    self.log.append(payload)
    if not self.module.check_mode:
      try:
        sat_resp = requests.post(
          hostvars['sat_api_url'],
          auth = (self.module.params['mgmtuser'], self.module.params['mgmtusrp']),
          headers = {"Content-Type": "application/json"},
          data = json.dumps(payload),
          verify = "/etc/pki/tls/certs/All-CA-bundle.pem",
          timeout = 60
        )
        sat_resp.raise_for_status()
        self.log.append(f"Host - {self.module.params['servername']} created successfully on Satellite - {hostvars['sat_host']}")
        self.log.append(sat_resp.json())
      except requests.exceptions.RequestException as e:
        self.log.append(f"Error Creating Host - {e}")
        if hasattr(e, 'response') and e.response is not None:
          self.log.append(f"ERROR Response content: {e.response.text}")
    else:
      self.log.append("Check Mode Enabled - No updates performed!")
    return

  def poweract(self, Srv):
    """Function to powercycle hardware to start PXE boot provisioining"""
    if Srv == "cisco":
      UCSDN = f"sys/chassis-{self.chassis}/blade-{self.blade}"
      ucsm_hndl = UcsHandle(self.module.params['servermgmt'], self.domusr, self.module.params['mgmtusrp'])
      ucsm_hndl.login()
      pwrstate = ucsm_hndl.query_dn(UCSDN)
      if pwrstate:
        self.log.append(f"Blade {UCSDN} Found.")
        pwrstate.admin_power = "cycle-immediate"
        ucsm_hndl.set_mo(pwrstate)
        ucsm_hndl.commit()
        self.log.append(f"{Srv} hardware Powercycle Initiates...")
      else:
        self.log.append(f"{Srv} hardware Powercycle Failed, Blade {UCSDN} not found!!")
      ucsm_hndl.logout()
    elif Srv == "dell":
      Ssh_pwr = SSHConn()
      pwrdellcmd = "racadm serveraction powercycle"
      sshresp = Ssh_pwr.do_ssh(self.module.params['servermgmt'], pwrdellcmd, self.domusr, self.module.params['mgmtusrp'])
      if "SSH Failed" in sshresp:
        self.log.append(f"{Srv} hardware Powercycle Failed...!!")
      else:
        self.log.append(f"{Srv} hardware Powercycle initiated...")
    return

  def checkerrors(self, err):
    """Function to detect errors in accumulated log entries"""
    found_err = list(filter(lambda x: err in x, self.log))
    return found_err

  def failfunc(self, chng=False):
    """Function to execute on failure"""
    self.results['msg'] = self.log
    self.results['changed'] = chng
    self.module.fail_json(**self.results)

  def exitfunc(self, chng=True):
    """Function to execute on graceful exit"""
    self.results['msg'] = self.log
    self.results['changed'] = chng
    self.module.exit_json(**self.results)

  def main(self):
    """Main Function for MainProg Class"""
    if self.module.params['cisco']:
      hrdw = "cisco"
      (mac. prinic, secnic) = self.getucsmac()
      extras = f"for Cisco Blade {self.blade} in Chassis {self.chassis}"
    elif self.module.params['dell']:
      hrdw = "dell"
      (mac, prinic, secnic) = self.getdellmac()
      extras = f"for Dell NIC Slot {self.nicslt}"
    else:
      (hrdw, mac, prinic, secnic, extras) = ("", "", "", "", "")
      self.log.append("Wrong Hardware Tyoe!!")
      self.failfunc(False)

    if mac:
      self.log.append(f"Primary NIC MAC Address {extras} is: {mac}")
      self.setuphost(hrdw, mac, prinic, secnic)
      host_errors = self.checkerrors("ERROR Creating Host")
      if host_errors:
        self.failfunc(False)
      elif not self.module.check_mode:
        time.sleep(3)
        self.log.append("\n")
        self.log.append(f"Powercycling {hrdw} hardware to start OS provisioning")
        self.poweract(hrdw)
        pwr_errors = self.checkerrors("Powercycle Failed")
        if pwr_errors:
          self.failfunc(True)
        self.exitfunc(True)
      else:
        self.exitfunc(False)
    else:
      self.log.append(f"Not able to extract Primary NIC MAC on {hrdw} hardware!!")
      self.failfunc(False)
    return


if __name__ == "__main__":
  provsrv = MainProg()
  provsrv.main()


                          


 