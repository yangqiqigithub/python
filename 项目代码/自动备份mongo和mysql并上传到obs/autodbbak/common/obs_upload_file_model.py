#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
模块使用方法
大前提：python3
1. 安装obs模块
    见华为云官方文档https://support.huaweicloud.com/sdk-python-devg-obs/zh-cn_topic_0142811715.html
2. 导入模块
    import obs_uplodfile （函数名）
3. 给函数传参
    参数介绍：
    :param ak: obs的Access Key
    :param sk: obs的Secret Key
    :param server: obs的endpoint地址
    :param bucketname: obs的名字
    :param localdir: 需要上传到obs本地目录，这个目录下应该都是文件或者压缩文件，不支持子目录
    :param obsdir_parent: 希望上传到obs后的目录名字 比如这里设置成mongodb_backup最终的备份目录为： mongodb_backup/2019-07/2019-07-08/


obs_uplodfile(ak='',
              sk='',
              server='',
              bucketname='',
              localdir='',
              obsdir_parent='')

'''


from config.settings import  BASEDIR
from common.recordlog import  Logger
import  os


def obs_uplodfile(ak,sk,server,bucketname,localdir,obsdir_parent):
    '''
    :param ak: obs的Access Key
    :param sk: obs的Secret Key
    :param server: obs的endpoint地址
    :param bucketname: obs的名字
    :param localdir: 需要上传到obs本地目录
    :param obsdir_parent: 希望上传到obs后的目录名字 比如这里设置成mongodb_backup最终的备份目录为： mongodb_backup/2019-07/2019-07-08/
    :return:
    '''

    from obs import ObsClient
    import os
    import time
    # 创建ObsClient实例
    obsClient = ObsClient(
        access_key_id=ak,
        secret_access_key=sk,
        server=server
    )

    DATE = time.strftime("%Y%m%d")

    MONTH = time.strftime("%Y%m")

    # 本地需要上传的目录 确保这个目录下都是文件 子目录不支持
    localdir = localdir
    # bucketname
    bucketname = bucketname
    Logger().log('开始上传到 %s OBS ...' %bucketname)
    # 设置分段上传时的最大并发数
    taskNum = 5
    # 设置分段大小为10MB
    partSize = 10 * 1024 * 1024
    # 开启断点续传模式
    enableCheckpoint = True

    # obs上存放数据的文件夹
    obsdir_parent=obsdir_parent
    obsdir = obsdir_parent  + '/' + MONTH + '/' + DATE  # mongodb_backup/2019-07/2019-07-08/

    # 规范整理文件名和文件绝对路径
    filename_list = []
    abspath_list = []
    for dir, _, file in os.walk(localdir):  # 变量解压
        filename_list = file
        for f in file:
            abspath = dir + "/" + f
            abspath_list.append(abspath)
    filename_abspath_list = zip(filename_list, abspath_list)
    for t in filename_abspath_list:
        # 设置待上传的本地文件，需要指定到具体的文件名
        uploadFile = t[1]
        objectName = t[0]
        # 进行断点续传上传
        try:
            # 创建obs存放数据的文件夹
            cdir = obsClient.putContent(bucketname, obsdir, content=None)
            obs_filepath = os.path.join(obsdir, objectName)
            resp = obsClient.uploadFile(bucketname, obs_filepath, uploadFile, partSize, taskNum, enableCheckpoint)
            Logger().log('%s开始上传' %objectName)
            if resp.status < 300:
                Logger().log('%s上传成功\n' %objectName)
                # content='status:', resp['status'], 'filename:', resp['body']['key']
            else:
                Logger().log('%s上传失败' %objectName,mode=False)
                #content= 'errorCode:', resp.errorCode, 'errorMessage:', resp.errorMessage
                # 操作失败时可再次调用断点续传上传接口进行重新上传
        except Exception as e:
            Logger().log('%s上传失败,发生错误%s' %(objectName,e), mode=False)

