#-------------------------------------------------------------------------------
# Name:        debug
# Purpose:
#
# Author:      shenhu1x
#
# Created:     11/09/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time

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


@debug
def test(x,y,z,a=0,b=1):
    for i in range(0,10):
        print i*x,i*y,i*z
        time.sleep(1)
    return 0

@debug
def main_test():
    test(1,2,3,a=0,b=4)

if __name__ == '__main__':
    main_test()
