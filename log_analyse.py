#-------------------------------------------------------------------------------
# Name:        log_analyse
# Purpose:
#
# Author:      shenhu1x
#
# Created:     10/10/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import re


def matched(line):
    return (re.match("", line))


def main():
    while True:
        line = sys.stdin.readline()
        if not data:
            break
        if matched(line):
            sys.stdout.write(line)

if __name__ == '__main__':
    main()
