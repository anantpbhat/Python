#!/usr/bin/python3

from ansible.module_utils.basic import *
from datetime import datetime, timedelta
import imp
import re
import atexit

server = 'vcenter.nj01'
password='big33l#23'
user='svc_vc_admin'
port=443

def findSnapshot(list, snap_name):

    for ea in list:
        if ea.name == snap_name:
            return ea
    if len(ea.childSnapshotList) > 0:
      ret = findSnapshot(ea.childSnapshotList, snap_name)
      if ret is not None:
            return ret
    return None


def main():

    fields = {
        "hostname": {"required": True, "type": "str"},
        "snap_name": {"required": False, "type": "str", "default": "2021-Patching" },
        "mem_switch": {"default": False, "type": "bool"},
    }

    module = AnsibleModule(argument_spec=fields)

    hostname = module.params['hostname']
    snap_name = module.params['snap_name']
    mem_switch = module.params['mem_switch']

    try:
        # check if the #module exists before trying to import it
        imp.find_module('pyVmomi')
        imp.find_module('pyVim')
        from pyVmomi import vmodl
        from pyVmomi import vim
        from pyVim import connect

    except ImportError as e:
        msg = 'is the module installed?'
        if module._verbosity >= 1:
            msg += "\n %s " % e
        module.fail_json(msg=msg)


    #Connect to the vSpere with the given information
    service_instance = connect.SmartConnectNoSSL(host=server, user=user, pwd=password, port=port)

    #Exit Handler to be executed at termination : Disconect from Vsphere
    atexit.register(connect.Disconnect, service_instance)

    #Set up variables used to build the container view
    content= service_instance.content
    #Starting search point
    root_folder = content.rootFolder
    #Search for Vm's
    viewType = [vim.VirtualMachine]
    recursive = True
    #Create the container view session with the vars:
    containerView = content.viewManager.CreateContainerView(root_folder, viewType, recursive)
    children = containerView.view


    #we need to append values from hostname to a list to work with
    vms = []
    if hostname is not None:
        # print(hostname)
        host =  hostname.replace(" ", "").rstrip()
        vms.append(host)

    '''
        children: List containing all of the vms
        vms: The list of vm names that were passed to the main function
    '''
    filtered_vms = []
    for vm in children:
        if vm.summary.config.name in vms:
            filtered_vms.append(vm)



    for vm in filtered_vms:
        if vm.snapshot is not None:
            snapshot = findSnapshot(vm.snapshot.rootSnapshotList, snap_name)
            if snapshot is not None:
                snapshot.snapshot.RemoveSnapshot_Task(removeChildren=False)
                print("Removed snapshot")
                module.exit_json(changed=True)
            else:
                module.exit_json(changed=False, msg="The Snapshot does not exist")
        else:
            module.exit_json(changed=False, msg="The Snapshot does not exist")



if __name__ == '__main__':
    main()
