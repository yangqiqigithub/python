#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang

import  subprocess
import os
from config.settings import save_days
import time
import  shutil
from config.settings import BASEDIR
from common.recordlog import  Logger
import configparser
def exec_shell_cmd(cmd):
    status,output=subprocess.getstatusoutput(cmd)
    if status == 0:
        return status,output
    else:
        Logger().log('%s命令执行错误' % (cmd), mode=False)
        raise Exception('%s命令执行错误' % (cmd))

# def write_log(dbkind,content):
#     '''
#     记录日志的函数
#     :param dbkind: 标识日志文件名字的一部分 比如设置成BqjMongo 最终的名字就是BqjMongo_20190711.log
#     :param content: 写入文件的内容
#     :return:
#     '''
#     DATE = time.strftime("%Y%m%d")
#     log_dir=BASEDIR + '/' + 'log' + '/'
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#     log_path=log_dir  +  dbkind+'_'+DATE+'.log'
#     with open(log_path,'a+',encoding='utf8') as f:
#         f.write(content)

def zipfile(target_dir,filepath):
    '''
    压缩文件或目录为zip压缩包
    :param filepath: 需要压缩的文件或者目录的绝对路径
    :param target_dir: 压缩到的目标目录
    :return:
    '''

    #                      压缩到哪             什么格式           压缩谁       glance2.zip 压缩后的样子
    #shutil.make_archive("E:\s14\day05\glance2", "zip", "E:\s14\day05\glance1")

    s=shutil.make_archive(target_dir,'zip',filepath)
    if s:
        shutil.rmtree(filepath)

    else:
        Logger().log('%s 压缩失败' %filepath, mode=False)

def clear_data(datapath):
    '''
    清理多余备份的函数
    :param datapath:
    :return:
    '''
    import time
    import  os
    import  shutil
    now_date=time.strftime("%Y%m%d")
    date7_ago=int(now_date)-save_days

    try:
        for dir in os.listdir(datapath):
            if dir:
                if int(dir) < date7_ago:
                    rm_dir_abspath=datapath + '/' + dir
                    shutil.rmtree(rm_dir_abspath)
                    Logger().log('清理过期的备份日期目录:%s' % rm_dir_abspath)
    except Exception as e:
        Logger().log('请勿在备份目录下放置除备份以外无关目录或者文件', mode=False)
        raise Exception('请勿在备份目录下放置除备份以外无关目录或者文件')



def parse():
    inifile_path = os.path.join(BASEDIR, 'config', 'dbinfo.ini')
    config = configparser.ConfigParser()
    config.sections()
    config.read(inifile_path, encoding='utf8')
    return config
