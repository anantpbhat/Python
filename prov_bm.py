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

