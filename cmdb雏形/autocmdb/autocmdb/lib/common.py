from autocmdb.settings import  HOSTSFILES_DIRS
from app import models
import time
import random
import string

def kb_GB(num):
    import re
    num=int(num.split('kB')[0].strip())
    result=str(int(num/1024/1024)) + 'GB'
    return result




def all_GB(num):

    if num[-1]=='B':
        dw=num[-2:len(num)]
        data=num[:-2]
        if dw=='TB':
            res= round(float(data)*1024)
        elif dw=='GB':
            res=round(float(data))
        elif dw=='MB':
            res=round(float(data)/1024)
        elif dw=='KB':
            res=round(float(data)*1024*1024)
        elif dw=='kB':
            res=round(float(data)*1024*1024)
        else:
            res=0
        return res

    else:
        dw=num[-1]
        data = num[:-1]
        if dw=='T':
            res= round(float(data)*1024)
        elif dw=='G':
            res=round(float(data))
        elif dw=='M':
            res=round(float(data)/1024)
        elif dw=='K':
            res=round(float(data)*1024*1024)
        elif dw=='k':
            res=round(float(data)*1024*1024)
        else:
            res=0
        return res



def clear_list(l):
    ll=[]
    for i in l:
        if i:
            ll.append(i)
    return ll



def savefile(obj):
    import os
    '''
    根据文件对象将文件保存在files目录下
    :param filename: 
    :return: 
    '''
    if not os.path.exists(HOSTSFILES_DIRS[0]):
        os.makedirs(HOSTSFILES_DIRS[0])
    file_abspath = os.path.join(HOSTSFILES_DIRS[0], obj.name)

    with open(file_abspath, 'wb') as f:
        for i in obj.chunks():
            f.write(i)
    if os.path.getsize(file_abspath)==0:
        pass
    else:
        return file_abspath

def insert_data(data_dict):
    models.HostsInfo.objects.create(**data_dict)

def create_unique_id():
    timestamp = str(int(time.time()))
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    unique_id = timestamp + ran_str
    return unique_id


def timestamp_strftime(t):
    strftime = time.strftime("%Y-%m-%d %H:%M", time.localtime(t))
    return strftime


def strftime_timestamp(t):
    timestamp=int(time.mktime(time.strptime(t, '%Y-%m-%d %X')))
    return timestamp
