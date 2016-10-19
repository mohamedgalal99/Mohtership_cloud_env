import JumpScale.grid
from JumpScale import j

cl = j.core.osis.getClientForNamespace('cloudbroker')
cl.cloudspace.simpleSearch({"status": "DEPLOYED", "location": "eu2"})
cl.vmachine.simpleSearch({"status": "RUNNING"})

css=cl.cloudspace.simpleSearch({"status": "DEPLOYED", "location": "eu1"})       #update location name
print '%10s %30s %10s %20s %20s' % ("vm", "vm_name", "stack", "cloudspace", "account")
print '\n'
for cs in css:
    account_id=cs.get('accountId')
    account_name = cl.account.get(account_id).name     # acount nanme
    cs_name = cs.get('name')     # cs name
    cs_id=cs.get('id')
    vms=cl.vmachine.simpleSearch({"cloudspaceId": cs_id, "status": "RUNNING"})
    for vm in vms:
        vm_hostname=vm.get("hostName")
        vm_name=vm.get("name")
        stackid=vm.get("stackId")
        stack_name=cl.stack.get(stackid).name
        print '%-10s\t%-30s\t%-10s\t%-30s\t%-20s' % (vm_hostname, vm_name, stack_name, cs_name, account_name)
        pass
