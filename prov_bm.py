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


class MainProd(BaseCl):
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
