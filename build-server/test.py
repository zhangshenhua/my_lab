#!/usr/bin/env python
import sys,traceback,os
#sys.path.append('/root/build-server/')
from framework import simplexml
from framework.common import *

from xml.etree.ElementTree import ElementTree

xml_config = simplexml.parse('config.xml')



class software(object):
    def __init__(self, str_software_id ):
        system = xml_config.system
        self.this_soft = xml_config.softwares.nodes[str_software_id]
        self.git  = str(self.this_soft.git)
        self.src_dir = \
            os.path.join(str(system.root_dir), 
                         str(system.repos_dir), 
                         str(self.this_soft.repo_dir))
        self.out_dir = \
            os.path.join(str(system.root_dir), 
                         str(system.out_dir), 
                         str(self.this_soft.out_dir))
        self.make_commands = str(self.this_soft.make_commands)
        self.install_commands = str(self.this_soft.install_commands)
        


a_soft = software('vgt_linux_kernel')
print a_soft.git
print a_soft.src_dir
print a_soft.out_dir
print a_soft.make_commands
print a_soft.install_commands



def this_server_ip():
    ip = os.popen("/sbin/ifconfig | grep 'inet addr' | awk '{print $2}'").read()
    ip = ip[ip.find(':')+1:ip.find('\n')]
    return ip

print this_server_ip()



print 'fdsfsdasfdsaf'
print try_get_xml_str(a_soft.this_soft,'git')
print try_get_xml_str(a_soft.this_soft,'git2')

def foo(a=1):
    print a

foo()



