#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang


import sys
import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from Plugin.mongobak import  mongodb_bak
from Plugin.mysqlbak import mysqldb_bak
from common.common import parse


bqj_mongo_host = parse()["mongo_info"]["host"]
bqj_mongo_port = parse()["mongo_info"]["port"]
bqj_mongo_user = parse()["mongo_info"]["user"]
bqj_mongo_pwd = parse()["mongo_info"]["pwd"]
bqj_mongo_bak_parent_path = parse()["mongo_info"]["bak_parent_path"]

bqj_mysql_host = parse()["mysql_info"]["host"]
bqj_mysql_port = parse()["mysql_info"]["port"]
bqj_mysql_user = parse()["mysql_info"]["user"]
bqj_mysql_pwd = parse()["mysql_info"]["pwd"]
bqj_mysql_bak_parent_path = parse()["mysql_info"]["bak_parent_path"]

def mongobak():
    mongodb_bak(host=bqj_mongo_host,
                port=bqj_mongo_port,
                user=bqj_mongo_user,
                pwd=bqj_mongo_pwd,
                bak_parent_path=bqj_mongo_bak_parent_path)
def mysqlbak():
    mysqldb_bak(host=bqj_mysql_host,
                port=bqj_mysql_port,
                user=bqj_mysql_user,
                pwd=bqj_mysql_pwd,
                bak_parent_path=bqj_mysql_bak_parent_path)
