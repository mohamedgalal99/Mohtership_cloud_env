import JumpScale.grid
import os
from JumpScale import j
cl = j.core.osis.getClientForNamespace('cloudbroker')
css = cl.cloudspace.simpleSearch({'status': 'DEPLOYED'})
for i in css:
    ip = i.get('publicipaddress')[:-3]
    print 'ROS: %s' % ip
    try:
        os.system('sshpass -p Dct007 ssh -p 9022 -o StrictHostKeyChecking=no vscalers@%s \'ip dns set allow-remote-requests=no\'' % ip)
#        os.system('sshpass -p Dct007 ssh -p 9022 -o StrictHostKeyChecking=no vscalers@%s \'ip dns print\'' % ip)
    except:
        print 'Can\'t connect to This ROS: %s' % ip
