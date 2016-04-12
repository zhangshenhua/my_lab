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
    """Call os.system(cmd_line) with log and return the result of os.system(cmd_line)."""
    g_logger.verbose('os.system cmd_line: %s' % cmd_line)
    result = os.system(cmd_line)
    g_logger.verbose('result: %s' % result)
    return result


def call_popen_with_timeout(cmd_line, timeout=120, use_call=True, use_shell=True, cwd=None):
    if use_call:
        cmd_line = "call " + cmd_line
    g_logger.verbose('subprocess.Popen cmd_line: %s' % cmd_line)
    g_logger.verbose('timeout value:', timeout)
    p = subprocess.Popen(cmd_line + ' 2>&1', shell=use_shell, cwd=cwd, stdout=subprocess.PIPE)
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
    g_logger.verbose('result: %s' % p.returncode)
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
    """
    make_cmdline('p1', 'p2', ...) = 'p1 p2 ...'
    """
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

# CASE PASS if result = 0
# CASE FAIL if other value
def case_exit(result):
    if result == 0:
        g_logger._Logger__result(True)
    else:
        g_logger._Logger__result(False)
    sys.exit(result)
	

def exit(status):
    dict_frame = private_lib.get_head_info(2)
    if isinstance(status, int):
        if status:
            g_logger.error('sys.exit({})'.format(status), dict_frame=dict_frame)
            g_logger._Logger__result(False)
        else:
            g_logger.verbose('sys.exit({})'.format(status), dict_frame=dict_frame)
            g_logger._Logger__result(True)
        sys.exit(status)
    else:
        if status == None:
            g_logger.verbose('sys.exit(0)'.format(status), dict_frame=dict_frame)
            g_logger._Logger__result(True)
            sys.exit(0)
        else:
            g_logger.error('{}'.format(status), dict_frame=dict_frame)
            g_logger.error('sys.exit(1)', dict_frame=dict_frame)
            g_logger._Logger__result(False)
            sys.exit(1)


def usage():
    g_logger.setid('COMMON_LIB_TEST')
    watch_start()  # TimeMarkStart
    g_logger.verbose('verbose infomation should not on screen, but in log file')
    g_logger.info('info infomation should not on screen, but in log file')
    g_logger.warn('warning infomation should on screen and in log file')
    g_logger.error('error infomation should on screen and in log file')
    call_os_system('dir c:')
    call_os_system(r'dir c:\not\a\dir')
    call_popen_with_timeout('dir c:')  # call_popen_with_timeout is more completely than call_os_system
    call_popen_with_timeout(r'dir c:\not\a\dir') # default timeout value is 2 minute.
    call_popen_with_timeout(r'sth.exe p1 p2 ...', 300)  # give 5 minute to run it, if no return machine will be reboot.
    watch_stop_and_print('this test')  # TimeMarkStop
    case_exit(0)
    case_exit(-1)  # this line will not be run


if __name__ == '__main__':
    usage()
