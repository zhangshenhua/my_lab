# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shenhu1x
#
# Created:     02/09/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import sys
import time
import common_lib


def main():
    """
    g_logger.setid('TEST_CASE_ID')
    g_logger.verbose('Protocol problem: %s', 'xxxfdsfdsfdsfafdfdfdsfx')
    g_logger.verbose("debug message")
    g_logger.info("info message")
    g_logger.info("info message", 'xxxxx')
    g_logger.warn("warn message")
    g_logger.error("error message")
    g_logger.warn("error message",'list1=%s list2=%s  ',[1,2,3],[4,5,6])
    g_logger.error([1,2,3])
    g_logger.error('command line time out!', 'cmd_line: %s', 'fdsfsd')
    g_logger.original('hello, would')
    g_logger.log(50,'fdsf')

    common_lib.call_popen_with_timeout('dir')

    g_logger.setid('TEST_CASE_ID')

    print('fdfdsf'
            'fdsfdsf')
    g_logger.case_pass()
    g_logger.case_fail()
    """
    for i in range(0, 1000):
        sys.stdout.write(str(i) * 4097 + '\n')
        time.sleep(0.001)

if __name__ == '__main__':
    main()
