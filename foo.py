#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     find command line from Scenarios
#
# Author:      shenhu1x
#
# Created:     17/09/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
from xml.etree.ElementTree import ElementTree


# ROOT_PATH = r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests'
ROOT_PATH = r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests\Check_In_Test'


def find_scenarios(keywords=[]):
    for (root, dirs,files ) in os.walk(ROOT_PATH):
        if 'Scenarios' in root:
            for file in files:
                file_path = os.path.join(root, file)
                if all([keyword in file_path for keyword in keywords]):
                    yield file_path


def find_cmdlines(filename):
    tree = ElementTree()
    tree.parse(filename)
    for cmd_line in [x.text for x in tree.findall('*//Parameters')]:
        yield cmd_line


def main():
    cmdline_set = set()
    for path in find_scenarios(['Camera']):
        print path
        for cmd_line in find_cmdlines(path):
            cmdline_set.add(cmd_line)
            print '    ' + str(cmd_line)
    print 'cmd_lines={'
    for cmdline in sorted(cmdline_set):
        print cmdline
    print '}'


if __name__ == '__main__':
        main()
