from JumpScale import j
import JumpScale.grid
cb = j.core.osis.getClientForNamespace('cloudbroker')
sys = j.core.osis.getClientForNamespace('system')

for accID in cb.account.list():
    user = cb.account.get(accID).name
    mail = sys.user.simpleSearch({'id': user})[0].get('emails')
    #credit = cb.creditbalance.simpleSearch({'accountId':accID})[-1].get('credit')
    credit = abs(sum(x['credit'] for x in cb.credittransaction.search({'accountId': accID, 'status': {'$ne': 'UNCONFIRMED'}})[1:]))
    css = ''
    css = cb.cloudspace.simpleSearch({'accountId': accID})
    print '\nUser: %s\tMail: %s\tCredit: %s' % (user,mail,credit)
    if css:
        for cs in css:
            if cs['status'] != 'DESTROYED':
                gid = cs['gid']
                status = cs['status']
                print '\n\tCloudspace: %s \tStatus: %s' % (cs['name'], status)
                vms = cb.vmachine.simpleSearch({'cloudspaceId': cs['guid']})
                orgnize = 1
                for vm in vms:
                    if vm['status'] != 'DESTROYED':
                        nameID = vm['id']
                        if orgnize > 4:
                            orgnize = 1
                            print '\t\tVM: vm-%s, name: %s, status: %s' %(nameID, vm[‘name’], vm['status'])
                        else:
                            print '\tVM: vm-%s, name: %S, status: %s' %(nameID, vm[‘name’], vm['status']),
                            orgnize+=1
