#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shenhu1x
#
# Created:     17/09/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
from xml.etree.ElementTree import ElementTree

def get_cmdlines(filename):
    try:
        tree = ElementTree()
        tree.parse(filename)
        return [x.text.strip() for x in tree.findall('*//Parameters')]
    except:
        return []


print_addition = 0
list_search_for = ['CameraDesktopBasicControl.py']

def main():
    result_list = []
    cmdline_set = set()
    for (root, dirs,files ) in os.walk(r'\\ccr\ec\proj\iag\mcg\SH_TSIE\AZ\TSIE_QA_TEST\CHT\batTests'):
        if 'Camera' in root and 'Scenarios' in dirs:
            for (root2,dirs2,files2) in os.walk(os.path.join(root,'Scenarios')):
                for file in files2:
                    cur_filename = os.path.join(root2,file)
                    result_list.append(cur_filename)
                    tmp_set = get_cmdlines(cur_filename)
                    tmp_set = filter(lambda cmdline:len(list_search_for)==0 or len([1 for search_item in list_search_for if str.lower(search_item) in str.lower(cmdline)])>0, tmp_set)
                    cmdline_set = cmdline_set.union(tmp_set)
                    if print_addition:
                        print cur_filename
                        for cmdline in tmp_set:
                            print '\t',cmdline

    print 'cmd_lines={'
    for cmdline in sorted(cmdline_set):
        print cmdline

    print '}'
    ##

if __name__ == '__main__':
    main()
