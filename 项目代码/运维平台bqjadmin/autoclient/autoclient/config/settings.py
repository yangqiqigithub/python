#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 错误日志
ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')

# Agent模式保存服务器唯一ID的文件
CERT_FILE_PATH = os.path.join(BASEDIR, 'config', 'cert')
#CERT_FILE_PATH="/etc/cert"

# 资产信息API
ASSET_API = "http://127.0.0.1:8000/api/asset/"

#指定监控的程序列表
server_list=['mongod','redis-server','java','mysqld','python3','nginx']

app_monitor_config={
    'mysqld':['3307','3306'],
    'redis-server':['6379'],
    'python3':['8001'],
    'mongod':['3717'],
    'postgres':[]
}