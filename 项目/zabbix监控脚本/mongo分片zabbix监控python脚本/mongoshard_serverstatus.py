#!/usr/local/python3/bin/python3
# -*- coding: utf-8 -*-
# Author qiqiYang


import subprocess
import sys
from pymongo import MongoClient
connect = MongoClient('mongodb://192.168.50.213:20000,192.168.50.205:20000,192.168.50.213:20000')

db = connect.admin
db.authenticate("monitoruser", "123")
command_dict = db.command('serverStatus')

uptime=int(command_dict['uptime'])
#1. 当前连接数
connects_current=command_dict['connections']['current']
#2. 连接数使用率
connects_available=command_dict['connections']['available']
connects_total=connects_available+connects_current
connects_utilization=connects_current/connects_total

#3. 每秒钟发送到数据库的数据量 M
bytesIn=round(command_dict['network']['bytesIn']/1024/1024/uptime,5)
#4.   每秒钟数据库发送出的数据量 M
bytesOut=round(command_dict['network']['bytesOut']/1024/1024/uptime,5)
#5.   每秒钟压缩后的物理实际进口流量 M
physicalBytesIn=round(command_dict['network']['physicalBytesIn']/1024/1024/uptime,5)
#6.   每秒钟压缩后的物理实际出口流量 M
physicalBytesOut=round(command_dict['network']['physicalBytesOut']/1024/1024/uptime,5)

#7.  每秒钟insert 执行的insert数量
insert_count=int(command_dict['opcounters']['insert'])/uptime
#8.  每秒钟 query 执行的query数量
query_count=int(command_dict['opcounters']['query'])/uptime
#9.   每秒钟update 执行的insert数量
update_count=int(command_dict['opcounters']['update'])/uptime
#10.   每秒钟delete 执行的update数量
delete_count=int(command_dict['opcounters']['delete'])/uptime
#11.   每秒钟getmore 执行的getmore数量
getmore_count=int(command_dict['opcounters']['getmore'])/uptime
#12.   每秒钟command 执行的command数量
command_count=round(int(command_dict['opcounters']['command'])/uptime,4)

#8. 使用内存大小 M
used_memeory=command_dict['mem']['resident']



if sys.argv[1]=='connects_current':
    print(connects_current)
elif sys.argv[1]=='connects_utilization':
    print(connects_utilization)
elif sys.argv[1]=='bytesIn':
    print(bytesIn)
elif sys.argv[1]=='bytesOut':
    print(bytesOut)
elif sys.argv[1]=='physicalBytesIn':
    print(physicalBytesIn)
elif sys.argv[1]=='physicalBytesOut':
    print(physicalBytesOut)
elif sys.argv[1]=='insert_count':
    print(insert_count)
elif sys.argv[1]=='query_count':
    print(query_count)
elif sys.argv[1]=='update_count':
    print(update_count)
elif sys.argv[1]=='delete_count':
    print(delete_count)
elif sys.argv[1]=='getmore_count':
    print(getmore_count)
elif sys.argv[1]=='command_count':
    print(command_count)
elif sys.argv[1]=='used_memeory':
    print(used_memeory)
else:
    pass







