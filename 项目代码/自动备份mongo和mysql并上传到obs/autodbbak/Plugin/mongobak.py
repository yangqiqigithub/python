#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang


from common.common import exec_shell_cmd
from common.common import zipfile
from common.common import  clear_data
from common.obs_upload_file_model import  obs_uplodfile
from common.common import parse
from common.recordlog import  Logger
import shutil
import  time
import os

def mongodb_bak(host,port,user,pwd,bak_parent_path):
    '''
    备份mongo数据库的函数
    功能如下：
    1.自动备份mongo库中所有数据库
    2. 将每个数据库压缩成zip压缩包
    3. 默认清理超过七天的数据
    :param host:  mongo数据库的ip
    :param port: mongo数据库的端口号
    :param user: mongo数据库的备份用户，此用户要有备份的权限和列出所有数据库名字的权限
    :param pwd: mongo数据库备份用户的密码
    :param bak_parent_path:  备份目录
    :return:
    '''


    Logger().log('Mongo 数据库备份开始...')
    DATE = time.strftime("%Y%m%d")
    MONTH = time.strftime("%Y%m")
    bakpath = bak_parent_path + MONTH + '/' + DATE + '/'
    if not os.path.exists(bakpath):
        os.makedirs(bakpath)


    # 拼接列出数据库名字的命令
    show_db_cmd = parse()['mongo_info']['mongo_cmd_path']  + ' ' + host + ':' + port + '/admin -u' + ' ' + user + ' ' + '-p' + ' ' + pwd \
                  + ' ' + '--eval "printjson(db.getMongo().getDBNames())"'

    # database_set 整理好的数据库名字集合
    status,dbname = exec_shell_cmd(show_db_cmd)
    database_set = set()
    for db in dbname.split('[')[1].split(']')[0].split('"'):
        database_set.add(db.strip(',').strip('\n\t').strip())
    database_set.remove('')
    database_set.remove('local')
    database_set.remove('admin')
    Logger().log('需要备份的Mongo数据库集合：%s' %database_set)

    # 开始备份
    for db in database_set:
        dump_cmd = parse()['mongo_info']['mongodump_cmd_path']  + ' ' + '--host' + ' ' + host + ':' + port + ' ' + '-u' + ' ' + user + ' ' + '-p' + ' ' + pwd + ' ' + \
                   '-d' + ' ' + db + ' ' + '-o' + ' ' + bakpath + ' ' + '--authenticationDatabase=admin'
        Logger().log('%s库 开始备份...'%(db))
        status, _ = exec_shell_cmd(dump_cmd)
        if status == 0:  # 0表示命令执行没问题
            path=bakpath+db
            zipfile(target_dir=path,filepath=path)
            content = '%s库 备份成功\n' % (db)
            Logger().log(content)
        else:
            content = '%s 备份失败' % (db)
            Logger().log(content,mode=False)
    Logger().log('Mongo数据库备份完毕')


    #开始清理过期的备份日期目录
    rm_dir=bak_parent_path + MONTH
    clear_data(rm_dir)

    #开始上传备份文件到obs
    obs_uplodfile(ak=parse()['obs_info']['ak'],
                  sk=parse()['obs_info']['sk'],
                  server=parse()['obs_info']['server'],
                  bucketname=parse()['obs_info']['bucketname'],
                  localdir=bakpath,
                  obsdir_parent=parse()['mongo_info']['obsdir_parent'])
    Logger().log('Mongo备份文件上传OBS完毕')






