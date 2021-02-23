#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging

BASEDIR = os.path.dirname(os.path.abspath(__file__))
# 错误日志
ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')

class Logger(object):


    def __init__(self):
        self.run_log_file = RUN_LOG_FILE
        self.error_log_file = ERROR_LOG_FILE
        self.run_logger = None
        self.error_logger = None

        self.initialize_run_log()
        self.initialize_error_log()

    @staticmethod
    def check_path_exist(log_abs_file):
        log_path = os.path.split(log_abs_file)[0]
        if not os.path.exists(log_path):
            os.mkdir(log_path)

    def initialize_run_log(self):
        self.check_path_exist(self.run_log_file)
        file_1_1 = logging.FileHandler(self.run_log_file, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)s :  %(message)s")
        file_1_1.setFormatter(fmt)
        logger1 = logging.Logger('run_log', level=logging.INFO)
        logger1.addHandler(file_1_1)
        self.run_logger = logger1

    def initialize_error_log(self):
        self.check_path_exist(self.error_log_file)
        file_1_1 = logging.FileHandler(self.error_log_file, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s  - %(levelname)s :  %(message)s")
        file_1_1.setFormatter(fmt)
        logger1 = logging.Logger('run_log', level=logging.ERROR)
        logger1.addHandler(file_1_1)
        self.error_logger = logger1

    def log(self, message, mode=True):
        """
        写入日志
        :param message: 日志信息
        :param mode: True表示运行信息，False表示错误信息
        :return:
        """
        if mode:
            self.run_logger.info(message)
        else:
            self.error_logger.error(message)




