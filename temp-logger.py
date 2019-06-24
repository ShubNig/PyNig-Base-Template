# -*- coding: utf-8 -*-
import getpass
import inspect
import logging
import logging.handlers
import optparse
import os
import platform
import sys
import time

__author__ = 'sinlov'

hint_help_info = """
must use faker by pip install requests
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


class PLog:
    def __init__(self):
        pass

    _runtime_version_error = """
This script must run python 2.6.+
"""

    ERROR = '\033[91m'
    OK_GREEN = '\033[96m'
    WARNING = '\033[93m'
    OK_BLUE = '\033[94m'
    HEADER = '\033[95m'
    WRITE = '\033[98m'
    BLACK = '\033[97m'
    END_LI = '\033[0m'

    _is_verbose = False

    logger = None
    """
    默认日志文件名
    """
    __log_folder = 'log'

    """
    自动清空日志的时间差，默认为一周
    """
    __out_of_time_log_auto_clean = 60 * 60 * 24 * 7

    @staticmethod
    def find_now_time_format(format_time=str):
        # type: (str) -> str
        """获取当前时间格式化的函数
        :param format_time:
        格式化参数:
          %y 两位数的年份表示（00-99）
          %Y 四位数的年份表示（000-9999）
          %m 月份（01-12）
          %d 月内中的一天（0-31）
          %H 24小时制小时数（0-23）
          %I 12小时制小时数（01-12）
          %M 分钟数（00=59）
          %S 秒（00-59）
          %a 本地简化星期名称
          %A 本地完整星期名称
          %b 本地简化的月份名称
          %B 本地完整的月份名称
          %c 本地相应的日期表示和时间表示
          %j 年内的一天（001-366）
          %p 本地A.M.或P.M.的等价符
          %U 一年中的星期数（00-53）星期天为星期的开始
          %w 星期（0-6），星期天为星期的开始
          %W 一年中的星期数（00-53）星期一为星期的开始
          %x 本地相应的日期表示
          %X 本地相应的时间表示
          %Z 当前时区的名称
          %% %号本身

        :return: time string
        """
        return time.strftime(format_time, time.localtime(time.time()))

    @staticmethod
    def check_dir_or_file_is_exist(abs_path=str):
        # type: (str) -> bool
        return os.path.exists(abs_path)

    @staticmethod
    def current_file_directory():
        """
        获取脚本文件执行目录
        :return:
        """
        path = os.path.realpath(sys.path[0])  # interpreter starter's path
        if os.path.isfile(path):  # starter is excutable file
            path = os.path.dirname(path)
            return os.path.abspath(path)  # return excutable file's directory
        else:  # starter is python script
            caller_file = inspect.stack()[1][1]  # function caller's filename
            return os.path.abspath(os.path.dirname(caller_file))  # return function caller's file's directory

    @staticmethod
    def check_current_log_path_and_auto_clean():
        """
        自动在脚本的运行目录创建 log 子目录，并检查日志文件，自动删除一周前的日志
        :return:
        """
        log_path = os.path.join(PLog.current_file_directory(), PLog.__log_folder)
        if not PLog.check_dir_or_file_is_exist(log_path):
            os.makedirs(log_path)
        else:
            check_time = time.time()
            for walk_dir, walk_folder, walk_file in os.walk(log_path):
                for f in walk_file:
                    if f.endswith('.log'):
                        check_path_join = os.path.join(walk_dir, f)
                        m_time = os.path.getmtime(check_path_join)
                        if check_time - m_time > PLog.__out_of_time_log_auto_clean:
                            os.remove(check_path_join)
                            print 'auto_clean log file : %s' % check_path_join
        return log_path

    @staticmethod
    def init_logger_by_time(tag=str):
        # type: (str) -> Logger
        PLog.logger = PLog.init_logger(tag, PLog.find_now_time_format('%Y_%m_%d_%H_%M_%S'))
        return PLog.logger

    @staticmethod
    def init_logger(first_tag, sec_tag=str):
        # type: (str, str) -> Logger
        log_file = first_tag + sec_tag + '.log'
        log_path = PLog.check_current_log_path_and_auto_clean()
        log_path_join = os.path.join(log_path, log_file)
        handler = logging.handlers.RotatingFileHandler(log_path_join, maxBytes=1024 * 1024, backupCount=5)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger = logging.getLogger(str(getpass.getuser()))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    @staticmethod
    def _is_sys_windows():
        return platform.system() == "Windows"

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
        if not PLog._is_sys_windows():
            print (PLog.WRITE + info + PLog.END_LI)
        else:
            print (info)
        if PLog.logger:
            PLog.logger.critical(info)

    @staticmethod
    def log_assert(info):
        if not PLog._is_sys_windows():
            print (PLog.BLACK + info + PLog.END_LI)
        else:
            print (info)
        if PLog.logger:
            PLog.logger.error(info)

    @staticmethod
    def log_info(info):
        if not PLog._is_sys_windows():
            print (PLog.OK_GREEN + info + PLog.END_LI)
        else:
            print (info)
        if PLog.logger:
            PLog.logger.info(info)

    @staticmethod
    def log_debug(info):
        if not PLog._is_sys_windows():
            print (PLog.OK_BLUE + info + PLog.END_LI)
        else:
            print (info)
        if PLog.logger:
            PLog.logger.debug(info)

    @staticmethod
    def log_warning(info):
        if not PLog._is_sys_windows():
            print (PLog.WARNING + info + PLog.END_LI)
        else:
            print (info)
        if PLog.logger:
            PLog.logger.warning(info)

    @staticmethod
    def log_error(info):
        if not PLog._is_sys_windows():
            print (PLog.ERROR + info + PLog.END_LI)
        else:
            print (info)
        if PLog.logger:
            PLog.logger.error(info)

    @staticmethod
    def log(msg, lev=str, must=False):
        # type: (str, str, bool) -> None
        if not PLog._is_sys_windows():
            if lev == 'i':
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


if __name__ == '__main__':
    PLog.check_runtime()
    now_folder_path = ''
    if len(sys.argv) < 2:
        PLog.log(enter_error_info, 'e', True)
        exit(1)
    # http://docs.python.org/library/optparse.html
    parser = optparse.OptionParser(
        '\n%prog ' + ' --tag 3\n' + hint_help_info)
    parser.add_option('-v', '--verbose', dest='v_verbose', action="store_true",
                      help="see verbose", default=False)
    (options, args) = parser.parse_args()

    PLog.init_logger_by_time(cwd_script_file_name.replace('.py', '-'))

    if options.v_verbose:
        PLog.set_verbose(options.v_verbose)
    PLog.log('info', 'i', True)
