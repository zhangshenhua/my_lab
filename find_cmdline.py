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
import re
from xml.etree.ElementTree import ElementTree


# ROOT_PATH = r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests'
SCENARIO_ROOT_PATHS = [
#    r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests\Check_In_Test',
    r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests\Daily_Regression',
    r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests\DryRun\Regular',
    r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests\DryRun\X64',
    r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests\Full_Regression\Ingredient_2014WW45',
]
SOURCE_ROOT_PATH = r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests\Camera\bat_All4\bat_common'


def list_files(dir, pattern='.*'):
    m = re.compile(pattern)
    for (root, dirs,files ) in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            if m.match(file_path):
                yield file_path


# cmd_line_keywords = map(lambda s: os.path.basename(s), list(list_files(SOURCE_ROOT_PATH, '.*\.py$')))
cmd_line_keywords = [
#    'CameraRaw.py',  #
#    'FeatureTestPerformanceDualCamDualPin.py',  #
#    'IVCameraDesktopModeTest.py',  #
    'StressTestVerification.py',
#    'stress_test.py',
#    'CopyLatestCameraDriver.py',
#    'DriverUninstall.py',
#    'enableDriverVerify.py',
#    'Binscope.py',
#    'ChkInfTest.py',
#    'ePac_Binscope.py',
#    'ePAC_Check_Unnecessary_driver_file.py',
#    'ePac_Unicode_Check.py',
#    'FlattenDriver.py',
#    'SymChkTest.py',
#    'CameraDCAAPI.py',
]

def find_scenarios(keywords=[]):
    for root_path in SCENARIO_ROOT_PATHS:
        for (root, dirs,files ) in os.walk(root_path):
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
            if any([filename in str(cmd_line) for filename in cmd_line_keywords]):
                cmdline_set.add(cmd_line)
                print '    ' + str(cmd_line)
    print 'cmd_lines={'
    for cmdline in sorted(cmdline_set):
        print cmdline
    print '}'


if __name__ == '__main__':
        main()
