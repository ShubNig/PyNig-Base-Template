#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import optparse

__author__ = 'sinlov'

reload(sys)
sys.setdefaultencoding('utf-8')

is_verbose = False
folder_path = os.getcwd()

hint_help_info = """
more information see
"""

cwd_script_file_name = sys.argv[0][sys.argv[0].rfind(os.sep) + 1:]
enter_error_info = """
Your input error
    Usage:
        python {0} --help
or input:
    ./{0} -h to see help
""".format(cwd_script_file_name)

runtime_version_error = """
This script must run python 2.6.+
"""


class PLog:
    def __init__(self):
        pass

    ERROR = '\033[91m'
    OK_GREEN = '\033[96m'
    WARNING = '\033[93m'
    OK_BLUE = '\033[94m'
    HEADER = '\033[95m'
    WRITE = '\033[98m'
    BLACK = '\033[97m'
    END_LI = '\033[0m'

    _runtime_version_error = """
This script must run python 2.6.+
"""
    _is_verbose = False

    @staticmethod
    def set_verbose(verbose=False):
        PLog._is_verbose = verbose

    @staticmethod
    def check_runtime():
        PLog.log('Python version %s' % platform.python_version(), 'd')
        version_split = platform.python_version().split('.')
        if version_split[0] != '2':
            PLog.log(PLog._runtime_version_error, 'e', True)
            exit(1)
        if version_split[1] < '6':
            PLog.log(PLog._runtime_version_error, 'e', True)
            exit(1)

    @staticmethod
    def log_normal(info):
        print (PLog.WRITE + info + PLog.END_LI)

    @staticmethod
    def log_assert(info):
        print (PLog.BLACK + info + PLog.END_LI)

    @staticmethod
    def log_info(info):
        print (PLog.OK_GREEN + info + PLog.END_LI)

    @staticmethod
    def log_debug(info):
        print (PLog.OK_BLUE + info + PLog.END_LI)

    @staticmethod
    def log_warning(info):
        print (PLog.WARNING + info + PLog.END_LI)

    @staticmethod
    def log_error(info):
        print (PLog.ERROR + info + PLog.END_LI)

    @staticmethod
    def log(msg, lev=str, must=False):
        # type: (str, str, bool) -> None
        if not platform.system() == "Windows":
            if lev == 'i':
                if PLog._is_verbose or must:
                    PLog.log_info('%s' % msg)
            elif lev == 'd':
                if PLog._is_verbose or must:
                    PLog.log_debug('%s' % msg)
            elif lev == 'w':
                PLog.log_warning('%s' % msg)
            elif lev == 'e':
                PLog.log_error('%s' % msg)
            elif lev == 'a':
                PLog.log_assert('%s' % msg)
            else:
                if PLog._is_verbose or must:
                    PLog.log_normal('%s' % msg)
        else:
            if lev == 'w' or lev == 'e':
                print('%s\n' % msg)
            else:
                if PLog._is_verbose or must:
                    print('%s\n' % msg)


def is_platform_windows():
    sys_str = platform.system()
    if sys_str == "Windows":
        return True
    else:
        return False


if __name__ == '__main__':
    PLog.check_runtime()
    folder_path = ''
    if len(sys.argv) < 2:
        PLog.log(enter_error_info, 'e', True)
        exit(1)
    parser = optparse.OptionParser('\n%prog ' + ' -p \n\tOr %prog <folder>\n' + hint_help_info)
    parser.add_option('-v', dest='v_verbose', action="store_true", help="see verbose", default=False)
    parser.add_option('-f', '--folder', dest='f_folder', type="string", help="path of folder Default is .",
                      default=".", metavar=".")
    parser.add_option('-l', '--level', dest='l_level', type="int", help="top level Default 7",
                      default=7, metavar=7)
    (options, args) = parser.parse_args()
    if options.v_verbose:
        is_verbose = True
    if options.l_level is not None:
        top_level = options.l_level
    if options.f_folder is not None:
        folder_path = options.f_folder
    if not is_verbose:
        # TODO delete this for dev
        print
        'todo what you want delete this'
        PLog.log("todo what you want before", 'w', True)
        exit(1)
    if not os.path.exists(folder_path):
        PLog.log("Error your input Folder %s is not exist" % folder_path, 'e', True)
        exit(1)
    if os.path.isdir(folder_path) < 1:
        PLog.log("Error your input path %s is not folder" % folder_path, 'e', True)
        exit(1)
