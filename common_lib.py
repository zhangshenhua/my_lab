# ------------------------------------------------------------------------------
# Name:        CommonLib
# Purpose:
#
# Author:      shenhu1x
#
# Created:     29/08/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
# ------------------------------------------------------------------------------
import subprocess
import sys
import time
import os
import re
import datetime
import inspect
import threading
import datetime

import private_lib

g_logger = private_lib.Logger()


def get_time():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

def debug(func):
    def _debug(*args, **kwargs):
        btime = time.time()
        print("%.3f %s begin." % (time.time(), func.__name__))
        print 'paras:{}{}'.format(args, kwargs)
        ret = func(*args, **kwargs)
        etime = time.time()
        print("%.3f %s end. during:%.3f result: %s" %
              (time.time(), func.__name__, etime-btime, ret))
        return ret
    return _debug


def decorator_print_cmdline(func, str_prefix):
    def _func(*args, **kwargs):
        print str_prefix, args[0]
        ret = func(*args, **kwargs)
        return ret
    return _func

subprocess.Popen = decorator_print_cmdline(subprocess.Popen, 'subprocess.Popen cmd_line = ')
os.system = decorator_print_cmdline(os.system, 'os.system cmd_line = ')


def enum(**enums):
    return type('Enum', (), enums)


"""
common_lib.watch_start()
clean_previous_driver()
common_lib.watch_stop_and_print('clean_previous_driver')
"""


def print_cmd_args():
    for i in range(len(sys.argv)):
        g_logger.info('argv{}: {}'.format(i, sys.argv[i]))


start_time = 0


def watch_start():
    global start_time
    start_time = time.time()
    g_logger.info("%.3f start_time." % (start_time))


def watch_stop_and_print(msg):
    global start_time
    stop_time = time.time()
    g_logger.info("%.3f stop_time." % (stop_time))
    g_logger.info('"{0}" duration: {1}s'.format(msg, stop_time - start_time))


def call_os_system(cmd_line):
    g_logger.info('os.system cmd_line: %s' % cmd_line)
    result = os.system(cmd_line)
    g_logger.info('result: %s' % result)
    return result


def call_popen_with_timeout(cmd_line, timeout=120, use_call=True, use_shell=True, cwd=None):
    if use_call:
        cmd_line = "call " + cmd_line
    g_logger.info('subprocess.Popen cmd_line: %s' % cmd_line)
    g_logger.info('timeout value:', timeout)
    p = subprocess.Popen(cmd_line, shell=use_shell, cwd=cwd, stdout=subprocess.PIPE)
    while True:
        time.sleep(1)
        timeout = timeout - 1
        g_logger.original(p.stdout.read())
        retval = p.poll()
        if retval is not None:
            break
        elif timeout <= 0:
            g_logger.error('command line timeout! will be reboot!', 'cmd_line: %s', cmd_line)
            call_popen_with_timeout('shutdown -r -t 0')
    g_logger.info('result: %s' % p.returncode)
    return p.returncode


def call_shell_get_stdout(cmd_line):
    g_logger.info('subprocess.Popen cmd_line: %s' % cmd_line)
    p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, shell=True)
    return p.communicate()[0]


def run_command_with_log(target, filename='result.log', timeout=120):
    # dir>a.txt|type a.txt
    filename = '"{}"'.format(filename)
    return call_popen_with_timeout(target + ' > ' + filename + ' 2>&1', timeout=timeout)


def get_time():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


def make_cmdline(*args):
    return reduce(lambda s1, s2: str(s1)+' '+str(s2), args)

def popen_with_continuation(cmd_line, co=lambda p: p):
    print 'subprocess.Popen cmd_line:', cmd_line
    p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, shell=True)
    return co(p)


def cond(ll):
    if len(ll) == 0:
        return None
    elif type(ll[0]) != type([]) or len(ll[0]) != 2:
        raise Exception('The form must be "cond([[p1, v1], ... , [pn, vn]])"')
    elif ll[0][0]:
        return ll[0][1]
    else:
        return cond(ll[1:])


def test():
    pass
    # print call_popen_with_timeout('python test.py')
    # print os.system('dir')
    '''
    g_logger.setid('TEST_CASE_ID')
    g_logger.verbose('Protocol problem: %s', 'connection reset')
    g_logger.verbose("debug message")
    g_logger.info("info message")
    g_logger.warn("warn message")
    g_logger.error("error message")
    g_logger.case_pass("very thing is ok.")
    g_logger.case_pass()
    g_logger.case_fail('something error. %i', -2)
    '''
    # os.chdir(r'c:/tmp')
    print call_popen_with_timeout('python test.py')


if __name__ == '__main__':
    test()
