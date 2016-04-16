#!/usr/bin/env python

"""This runs 'ls -l' on a remote host using SSH. At the prompts enter hostname,
user, and password.

$Id: sshls.py 489 2007-11-28 23:40:34Z noah $
"""
import time
import pexpect, pxssh
import os, sys, traceback

def ssh_command (host, user, password, command):

    """This runs a command on the remote host. This could also be done with the
pxssh class, but this demonstrates what that class does at a simpler level.
This returns a pexpect.spawn object. This handles the case when you try to
connect to a new host and ssh asks you if you want to accept the public key
fingerprint and continue connecting. """
    ssh_newkey = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s'%(user, host, command))
    i = child.expect([pexpect.EOF, pexpect.TIMEOUT, ssh_newkey, 'password: '])
    if i == 0:
        return child
    if i == 1: # Timeout
        print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None
    if i == 2: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        child.expect ('password: ')
        child.sendline(password)
    if i == 3:
            child.sendline(password)
    time.sleep(1)
    return child
    
def main ():
    child = ssh_command (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print child.before

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(1)

