#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang


import  os
import  time
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_days=7  #备份保留天数
DATE = time.strftime("%Y%m%d")
# 错误日志
errorlog='error'+DATE+'.log'
ERROR_LOG_FILE = os.path.join(BASEDIR, "log", errorlog)
# 运行日志
runlog='run'+DATE+'.log'
RUN_LOG_FILE = os.path.join(BASEDIR, "log", runlog)