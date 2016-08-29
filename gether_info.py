from JumpScale import j
import JumpScale.portal
import commands

env = 'ca1'
fw = ['fw1','fw2', 'fw3']
cl = j.core.osis.getClient(user='root')
cloudspacecl =  j.core.osis.getClientForCategory(cl, 'cloudbroker', 'cloudspace')
vmachinecl = j.core.osis.getClientForCategory(cl, 'cloudbroker', 'vmachine')
sizecl = j.core.osis.getClientForCategory(cl, 'cloudbroker', 'size')
imagecl = j.core.osis.getClientForCategory(cl, 'cloudbroker', 'image')
stackcl = j.core.osis.getClientForCategory(cl, 'cloudbroker', 'stack')

#for i in cloudspacecl.simpleSearch({"location": "ca1"}):
#    cloudspacecl.simpleSearch({"location": "ca1"})[i].get('guid')
#    print i

#Number of Cloud Spaces
c = 0
for i in cloudspacecl.simpleSearch({"location": "%s" % env}):
#    print i.get('guid')
    c = c + 1
print "Number of Cloud Spaces: %s" % c

#Number of Virtual Machines
m = 0
for i in cloudspacecl.simpleSearch({"location": env}):
    cs = i.get('guid')
    m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "RUNNING"}))
    m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "HALTED"}))
    m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "SUSPENDED"}))
print "Number of Virtual Machines: %s" % m

#Most popular OS Image running
m=0
images = [1,2,3,4,6,13,14,15,16,23,29,43]
print "\tMost popular OS Image for running VMs ..."
for img in images:
    for i in cloudspacecl.simpleSearch({"location": env}):
        cs = i.get('guid')
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "RUNNING", "imageId": img}))
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "HALTED", "imageId": img}))
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "SUSPENDED", "imageId": img}))
    imgName = imagecl.get(img).name
    print "image [%s] has: %s" % (imgName, m)
    m = 0

#Most popular OS Image
m=0
images = [1,2,3,4,6,13,14,15,16,23,29,43]
print "\tMost popular OS Image ..."
for img in images:
    for i in cloudspacecl.simpleSearch({"location": env}):
        cs = i.get('guid')
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "imageId": img}))
    imgName = imagecl.get(img).name
    print "image [%s] has: %s" % (imgName, m)
    m = 0

#Most popular image package RUNNING
m = 0
s = [1,2,3,4,5,6]
print "\tMost popular image package for RUNNING VMs..."
for size in s:
    for i in cloudspacecl.simpleSearch({"location": env}):
        cs = i.get('guid')
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "RUNNING", "sizeId": size}))
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "HALTED", "sizeId": size}))
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "SUSPENDED", "sizeId": size}))
    memory = sizecl.get(size).memory
    print "Size %s has: %s" % (memory, m)
    m = 0

#Most popular image package
m = 0
s = [1,2,3,4,5,6]
print "\tMost popular image package ..."
for size in s:
    for i in cloudspacecl.simpleSearch({"location": env}):
        cs = i.get('guid')
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "sizeId": size}))
    memory = sizecl.get(size).memory
    print "Size %s has: %s" % (memory, m)
    m = 0

# Get total memory used
m = 0
total = 0
s = [1,2,3,4,5,6]
print "\tGet total memory used ..."
for size in s:
    for i in cloudspacecl.simpleSearch({"location": env}):
        cs = i.get('guid')
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "RUNNING", "sizeId": size}))
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "HALTED", "sizeId": size}))
        m = m + len(vmachinecl.simpleSearch({"cloudspaceId": cs, "status": "SUSPENDED", "sizeId": size}))
    memory = sizecl.get(size).memory
    if size == 3:
        mem512 = m * 4
    elif size == 4:
        mem512 = m * 8
    elif size == 5:
        mem512 = m * 16
    elif size == 6:
        mem512 = m * 32
    else:
        mem512 = m * size
    total = total + mem512
    print "size %s has: %s \t 512 =  %s" % (memory, m, mem512)
    m = 0
tot = total * 512
print "total machines running as 512M ram: %s and consume %sM" % (total, tot)
#Get total memory of nodes in stack
nodes = stackcl.list()
for i in nodes:
    cpu = stackcl.get(i).referenceId
    if env == 'ca1':
        com = 'ssh root@%s.york1.vscalers.com cat /proc/meminfo | grep MemTotal | awk {\'print $2\'}' % cpu
    elif env == 'us1':
        com = 'ssh root@%s.lenoir2.vscalers.com cat /proc/meminfo | grep MemTotal | awk {\'print $2\'}' % cpu
    out = commands.getoutput(com)
    total = total + int(out)

os = len(nodes) * 2
total = (total / 1024) -os
free = total - tot
available_machines = free/512
print "Total amount of memory:%sM" % total
print "Free memory: %sM" % free
print "Amount of VMs 512 can be created: %s" % available_machines
#Routeros
print 'Calculation for how many routeros can be created based only on memory and I assume that each on will use 40M(in routeros config we make its ram 128M and used from it is 20M only) and their are other consideration such processor which doesn\'t calculated'
total = 0
num_ros = 0
for i in fw:
        if env == 'ca1':
                com = 'ssh root@%s.york1.vscalers.com cat /proc/meminfo | grep MemTotal | awk {\'print $2\'}' % i
                com2 = 'ssh root@%s.york1.vscalers.com virsh list --all | grep routeros | wc -l' % i
        elif env == 'us1':
                com = 'ssh root@%s.lenoir2.vscalers.com cat /proc/meminfo | grep MemTotal | awk {\'print $2\'}' % i
                com2 = 'ssh root@%s.lenoir2.vscalers.com virsh list --all | grep routeros | wc -l' % i
        mem = commands.getoutput(com)
        total = total + int(mem)
        num_ros = num_ros + int(commands.getoutput(com2))
total_MB = total/1024
routeros_can_create = (total_MB / 40) - num_ros
print 'Firewall total memory: %sMB' % total_MB
print 'Number of routeros : %s' % num_ros
print 'Number of Routeros can be created (if each router make 40MB basy): %s' % routeros_can_create

