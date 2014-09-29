#-------------------------------------------------------------------------------
# Name:        tee.py
# Purpose:
#
# Author:      shenhu1x
#
# Created:     24/09/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os,sys
def main():
    filename = sys.argv[1]
    with open(filename, "w") as f:
        while True:
            data = sys.stdin.read(1)
            if not data:
                break
            f.write(data)
            sys.stdout.write(data)


if __name__ == '__main__':
    main()