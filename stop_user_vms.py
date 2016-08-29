# create file stop.txt and put in it accounts which u need to stop their machines in nodes

from JumpScale import j
import fileinput
import JumpScale.portal
import commands

cl = j.core.osis.getClient(user='root')
accountcl = j.core.osis.getClientForCategory(cl, 'cloudbroker', 'account')
cloudspacecl =  j.core.osis.getClientForCategory(cl, 'cloudbroker', 'cloudspace')
vmachinecl = j.core.osis.getClientForCategory(cl, 'cloudbroker', 'vmachine')
stackcl = j.core.osis.getClientForCategory(cl, 'cloudbroker', 'stack')

loc = 'ca1'
#loc = 'us1'
#action = 'suspend'
#action = 'resume'
action = 'destroy'
#action = 'undefine'
#action = 'strat'
env = ''
status = ['RUNNING', 'HALTED', 'PAUSED']
#Read from file, each line contain user login name
#lines = open('pause.txt').read().splitlines()
lines = open('stop.txt').read().splitlines()
for line in lines:
    if len(accountcl.simpleSearch({'name': line})) == 1:
        #get account guid
        account_guid = accountcl.simpleSearch({'name': line})[0].get('guid')
        #Search about CSs belong to user
        for len_cs in xrange (0, len(cloudspacecl.simpleSearch({'accountId': account_guid}))):
            cs_guid = cloudspacecl.simpleSearch({'accountId': account_guid})[len_cs].get('guid')
            cs_location = cloudspacecl.simpleSearch({'accountId': account_guid})[len_cs].get('location')
            for stat in status:
                vmNum = len(vmachinecl.simpleSearch({'cloudspaceId': cs_guid, 'status': stat}))
                if cs_location == loc:
                    if vmNum <> 0:
                        for len_vm in xrange (0, vmNum):
                            vm_guid = vmachinecl.simpleSearch({'cloudspaceId': cs_guid, 'status': stat})[len_vm].get('guid')
                            vm = vmachinecl.get(vm_guid)
                            vm_hostname = vm.hostName
                            vm_stack = vm.stackId
                            cpu = stackcl.get(vm.stackId).referenceId
                            if loc == 'ca1':
                                env = 'york1'
                            elif loc == 'us1':
                                env = 'lenoir2'
                            command = 'ssh root@%s.%s.vscalers.com virsh %s %s' % (cpu, env, action, vm_hostname)
#                            print 'user\t:%s\t cloudspace id:%s\t location:%s\t command:%s' % (line, cs_guid, cs_location, command)
                            try:
                                out = commands.getoutput(command)
                                print out
                            except:
                                print 'fail, %s' % command
                        
                    
    elif len(accountcl.simpleSearch({'name': line})) == 0:
        print 'No Account with name: %s' % line
    else:
        print 'Multi account with name: %s' % line


