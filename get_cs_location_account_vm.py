import JumpScale.portal
from JumpScale import j
cl = j.core.osis.getClientForNamespace('cloudbroker')
css = cl.cloudspace.simpleSearch({'location': 'ca1', 'status': 'DEPLOYED'})
len(css)
for i in css:
    account = cl.account.get(i.get('accountId')).name
    print account,
    print i.get('name')
    id = i.get('id')
    vms = cl.vmachine.simpleSearch({'cloudspaceId': id, 'status': 'RUNNING'})
    for vm in vms:
        print "\t %s" % vm.get('name')
