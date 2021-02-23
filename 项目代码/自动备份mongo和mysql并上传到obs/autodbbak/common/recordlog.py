#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
使用方法：
1.导入模块
    from xxx.record_log import Logger
2. 实例化对象写入日志
    Logger().log('我是运行日志') #默认写入运行日志文件run.log
    Logger().log('我是错误日志',mode=False) #mode=False 写入错误日志文件 error.log

3. 日志内容大概如下：
    error.log
        2017-02-22 18:10:43,275  - ERROR :  API授权失败
    run.log
        2017-02-22 16:46:31,255 - INFO :  Success
4. 日志文件路径的规划化
    这里我把日志文件的路径规划直接写在了这个py文件里，但是对于一个项目而言，这种路径一般还在settings.py
    文件里规划好
    settings.py参考配置：

    import os
    BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 错误日志
    ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')
    # 运行日志
    RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')

    在settings.py里设置好后，应该在此文件中导入，导入方式参考配置：

    from config import settings

    class Logger(object):
        __instance = None

        def __init__(self):
            self.run_log_file = settings.RUN_LOG_FILE #这里也应该修改成导入的路径
            self.error_log_file = settings.ERROR_LOG_FILE

    然后此文件中的以下几行删除或者注释即可
    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    # 错误日志
    ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')
    # 运行日志
    RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')

'''


import os
import logging
from config import settings

class Logger(object):


    def __init__(self):
        self.run_log_file = settings.RUN_LOG_FILE
        self.error_log_file = settings.ERROR_LOG_FILE
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




