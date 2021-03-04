



#脚本跑在windows系统上
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang
import paramiko
import datetime
import os
import shutil
import time

#Linux远端服务器的信息
hostname = '192.168.33.1'
username = 'xxxx'
password = 'xxx'
port = 22

#将window上需要上传的目录备份到另一个路径
def cpbakdir(localdir,cp_dir):
    if not os.path.exists(cp_dir):
        shutil.copytree(local_dir, cp_dir)
    else:
        print('本地备份目录%s已经存在，请手动检查' %(cp_dir))

#windows目录覆盖Linux前，先将Linux上的目录备份
def  bakremotedir():
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    # 执行命令
    cmd = 'cp -a' + ' ' + remote_dir + ' ' + remote_dir_bakdir
    print('远程备份路径为%s' %(remote_dir_bakdir))

    stdin, stdout, stderr = ssh.exec_command(cmd)
    ssh.close()

#上传win上的文件覆盖到Linux上
def upload(local_dir, remote_dir):
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)

        print('upload file start %s ' % datetime.datetime.now())

        for root, dirs, files in os.walk(local_dir):

            #print('[%s][%s][%s]' % (root, dirs, files))
            for filespath in files:
                local_file = os.path.join(root, filespath)
                #print(11, '[%s][%s][%s][%s]' % (root, filespath, local_file, local_dir))
                a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
                #print('01', a, '[%s]' % remote_dir)
                remote_file = os.path.join(remote_dir, a)
                #print(22, remote_file)
                try:
                    sftp.put(local_file, remote_file)
                except Exception as e:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file, remote_file)
                    print("66 upload %s to remote %s" % (local_file, remote_file))
            for name in dirs:
                local_path = os.path.join(root, name)
                #print(0, local_path, local_dir)
                a = local_path.replace(local_dir, '').replace('\\', '')
                #print(1, a)
                #print(1, remote_dir)
                remote_path = os.path.join(remote_dir, a)
                #print(33, remote_path)
                try:
                    sftp.mkdir(remote_path)
                    #print(44, "mkdir path %s" % remote_path)
                except Exception as e:
                    #print(55, e) 这个只是创建目录的错误 不用理会
                    pass
        print('77,upload file success %s ' % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(88, e)
        
if __name__ == '__main__':
    local_dir = r'E:\CACC1111'  #windows上本地需要上传的目录 
    t = time.strftime("%Y%m%d")
    cp_dir = os.path.join('E:\\1028', t) #windows上备份上传目录的目录
    remote_dir = '/tmp/test/' #linux远程服务器上需要被覆盖的目录
    remote_dir_bakdir = '/tmp/' + 'bak' + '_' + t #Linux被覆盖前备份的路径 效果如下 /tmp/bak_20190220
    bakremotedir()
    #cpbakdir(local_dir, cp_dir) #windows本地就不做备份了 没必要
    upload(local_dir, remote_dir)


