# -------------------------------------------------------------------------------
# Name:        private_lib.py
# Purpose:
#
# Author:      shenhu1x
#
# Created:     21/10/2014
# Copyright:   (c) shenhu1x 2014
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import os
import sys
import logging
import datetime


def mkdirs(s):
    if not os.path.isdir(s):
        os.makedirs(s)
    return s


def get_head_info(depth):
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame
        for i in range(depth):
            if f.f_back is None:
                break
            f = f.f_back
    return {'file': os.path.basename(f.f_code.co_filename),
            'func': f.f_code.co_name,
            'line': str(f.f_lineno)}


def fmt_now():
    'mm/dd/yyyy-hh:mm:ss.ms'
    return datetime.datetime.strftime(
        datetime.datetime.now(),
        '%m/%d/%Y-%H:%M:%S.%f')[:-3]


class Logger(logging.getLoggerClass()):
    str_id = ''
    log_dir = mkdirs(r'C:\AutoBAT Results\TestLogs')
    '''
    VERBOSE, INFO, WARNING, ERROR, RESULT
    '''
    def __init__(self):
        super(Logger, self).__init__(Logger.str_id)
        self.setLevel(logging.DEBUG)
        self.__fh = logging.FileHandler("{0}.log".format(os.path.join(Logger.log_dir, 'default')))
        self.addHandler(self.__fh)
        self.__ch = logging.StreamHandler()
        self.addHandler(self.__ch)

    def setid(self, str_id):
        Logger.str_id = str_id
        self.removeHandler(self.__fh)
        self.__fh = logging.FileHandler("{0}.log".format(os.path.join(Logger.log_dir, Logger.str_id)))
        self.addHandler(self.__fh)

    def original(self, msg,  *argv, **argd):
        self.log(logging.DEBUG, msg, *argv, **argd)

    def __log(self, category, msg, opt='', *argv, **argd):
        """
        [mm/dd/yyyy-hh:mm:ss.ms][Category][File:xxx.py][Method:xxx_xxx][Line:xx][Primary: info message]
        [mm/dd/yyyy-hh:mm:ss.ms][Category][File:xxx.py][Method:xxx_xxx][Line:xx][Primary: info message][Optional: info message]
        str_lvl in {VERBOSE, INFO, WARNING, ERROR, RESULT}
        """
        dict_frame = get_head_info(3)
        self.original(
            '{time}{category}{file}{method}{line}{primary}{optional}'.format(
                time='[{}]'.format(fmt_now()),
                category='[{}]'.format(category),
                file='[File:{}]'.format(dict_frame['file']),
                method='[Method:{}]'.format(dict_frame['func']),
                line='[Line:{}]'.format(dict_frame['line']),
                primary='[Primary: {}]'.format(msg),
                optional='[Optional: {}]'.format(opt) if opt else '',
            ),
            *argv, **argd
        )

    def __result(self, is_pass):
        """
        [mm/dd/yyyy-hh:mm:ss.ms][RESULT][File:xxx.py][Method:xxx_xxx][Line:xx][Result: pass]
        """
        dict_frame = get_head_info(3)
        self.original(
            '{time}{category}{file}{method}{line}{result}'.format(
                time='[{}]'.format(fmt_now()),
                category='[RESULT]',
                file='[File:{}]'.format(dict_frame['file']),
                method='[Method:{}]'.format(dict_frame['func']),
                line='[Line:{}]'.format(dict_frame['line']),
                result='[Result: {}]'.format('pass' if is_pass else 'fail')
            )
        )

    def verbose(self, msg, opt='', *argv, **argd):
        self.__log('VERBOSE', msg, opt, *argv, **argd)

    def info(self, msg, opt='', *argv, **argd):
        self.__log('INFO', msg, opt, *argv, **argd)

    def warn(self, msg, opt='', *argv, **argd):
        self.__log('WARNING', msg, opt, *argv, **argd)

    def error(self, msg, opt='', *argv, **argd):
        self.__log('ERROR', msg, opt, *argv, **argd)

    def case_pass(self):
        self.__result(True)

    def case_fail(self):
        self.__result(False)


def main():
    pass

if __name__ == '__main__':
    main()
