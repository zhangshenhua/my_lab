#-------------------------------------------------------------------------------
# Name:        watch
# Purpose:
#
# Author:      shenhu1x
#
# Created:     11/10/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import os
import time


def make_cmdline(*args):
    return reduce((lambda s1, s2: str(s1) + ' ' + str(s2)), args, 'call')


def main():
    t1 = time.time()
    print 'start time:', t1
    cmd_line = make_cmdline(*sys.argv[1:])
    print 'cmd_line = ', cmd_line
    result = os.system(cmd_line)
    t2 = time.time()
    print 'end time:',t2
    print 'duration: %fs' % (t2 - t1)
    exit(result)

if __name__ == '__main__':
    main()
