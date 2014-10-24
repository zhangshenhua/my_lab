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
from common_lib import g_logger


def main():
    g_logger.setid('TEST_CASE_ID')
    g_logger.verbose('Protocol problem: %s', 'xxxx')
    g_logger.verbose("debug message")
    g_logger.info("info message")
    g_logger.info("info message", 'xxxxx')
    g_logger.warn("warn message")
    g_logger.error("error message")
    g_logger.error("error message",'value:1')
    g_logger.case_pass()
    g_logger.case_fail()

if __name__ == '__main__':
    main()
