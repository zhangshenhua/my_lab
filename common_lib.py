#-------------------------------------------------------------------------------
# Name:        CommonLib
# Purpose:
#
# Author:      shenhu1x
#
# Created:     29/08/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import subprocess
import sys
import time
import os
import re

def debug(func):
    def _debug(*args, **kwargs):
        btime = time.time()
        print("%.3f %s begin."%(time.time(),func.__name__))
        print 'paras:{}{}'.format(args,kwargs)
        ret = func(*args, **kwargs)
        etime = time.time()
        print("%.3f %s end. during:%.3f result: %s"%(time.time(),func.__name__,etime-btime,ret))
        return ret
    return _debug

def call_os_system(cmd_line):
    print 'cmd_line:',cmd_line
    result = os.system(cmd_line)
    print 'result:',result
    return result

def run_command(target,use_call=True,use_shell=True,cwd=None):
    if use_call:
        target = "call " + target
    process = subprocess.Popen(target,shell=use_shell,cwd=cwd)
    process_count = 0
    while True:
        time.sleep(3)
        retval = process.poll()
        if retval is not None:
            break
        else:
            time.sleep(10)
            process_count+=1
            if process_count > 12:
                os.system('shutdown -r -t 0')
    return process.returncode

def run_command_with_log(target,filename='result.log'):
    #dir>a.txt|type a.txt
    filename = '"{}"'.format(filename)
    return run_command(target + ' > '+ filename + ' 2>&1' )  # + '|type ' + filename

def get_time():
    return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))


def call_popen_with_timeout(cmd_line,timeout=120,timeout_do=lambda :call_os_system('shutdown -r -t 0'),use_call=True,use_shell=True,cwd=None):
    if use_call:
        cmd_line = "call " + cmd_line
    process = subprocess.Popen(cmd_line,shell=use_shell,cwd=cwd)
    process_count = 0
    while True:
        time.sleep(1)
        retval = process.poll()
        if retval is not None:
            break
        else:
            process_count+=1
            if process_count > timeout:
                timeout_do()
    return process.returncode

@debug
def test():
    #os.chdir(r'c:/TEMP')

    #print call_popen_with_timeout('python test.py',10,lambda:call_os_system('echo timeout!'))
    print os.system('dir')

os.system=debug(os.system)

if __name__ == '__main__':
    test()
