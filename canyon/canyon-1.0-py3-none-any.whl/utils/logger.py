# -*- coding : utf-8 -*-
# @Time   : 2021/9/29 22:20
# @Author : goodli
# @File   : logger.py
# @Project: Valley 山谷

import logging
import os.path
import time
from colorama import Fore, Style
import sys
import inspect


class Logger(object):
    def __init__(self, logger="logger", logfile="", level=logging.DEBUG):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        :param logger:  定义对应的程序模块名name，默认为root
        """

        # 创建一个logger
        self.logger = logging.getLogger(name=logger)
        self.logger.setLevel(level)  # 指定最低的日志级别 critical > error > warning > info > debug
        self.logger.propagate = False
        
        # 创建一个handler，用于写入日志文件
        #rq = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        #log_path = os.getcwd() + "/logs/"
        #log_name = log_path + rq + ".log"
        #formatter = logging.Formatter(
        #    "[%(asctime)s][l:%(lineno)d]-%(message)s")
        #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志，解决重复打印的问题
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "[%(asctime)s.%(msecs)03d][%(caller)s]-%(message)s", "%Y%m%d-%H%M%S")

            if logfile != "":
                fh = logging.FileHandler(logfile, mode='w')
                fh.setLevel(level)
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)
            else:
                # 创建一个handler，用于输出到控制台
                ch = logging.StreamHandler(sys.stdout)
                ch.setLevel(level)
                ch.setFormatter(formatter)
                self.logger.addHandler(ch)

    def get_caller(self):
        frames = inspect.stack()
        _, file_path, lineno, func_name, _, _ = frames[2]
        filename = os.path.basename(file_path)
        return "{}:{:03d}".format(filename, lineno)

    def debug(self, msg):
        """
        定义输出的颜色debug--white，info--green，warning/error/critical--red
        :param msg: 输出的log文字
        :return:
        """
        self.logger.debug(Fore.WHITE + "DEBUG-" + str(msg) + Style.RESET_ALL, extra={'caller': self.get_caller()})

    def info(self, msg):
        self.logger.info(Fore.GREEN + "INFO-" + str(msg) + Style.RESET_ALL, extra={'caller': self.get_caller()})

    def warning(self, msg):
        self.logger.warning(Fore.RED + "WARNING-" + str(msg) + Style.RESET_ALL, extra={'caller': self.get_caller()})

    def error(self, msg):
        self.logger.error(Fore.RED + "ERROR-" + str(msg) + Style.RESET_ALL, extra={'caller': self.get_caller()})

    def critical(self, msg):
        self.logger.critical(Fore.RED + "CRITICAL-" + str(msg) + Style.RESET_ALL, extra={'caller': self.get_caller()})


if __name__ == '__main__':
    log = Logger(logger="t", level=logging.DEBUG)
    log.debug("debug")
    log.info("info")
    log.error("error")
    log.warning("warning")
    log.critical("critical")