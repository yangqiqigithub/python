# 日志级别
```
CRITICAL = 50 #FATAL = CRITICAL
ERROR = 40
WARNING = 30 #WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0 #不设置

默认级别为 WARNING默认打印到终端 默认是root
```
```
import logging

logging.debug("debug信息")
logging.info("info信息")
logging.warning("warning警告信息")
logging.error("error错误信息")
logging.critical("critical严重危险灾难信息")
'''
默认是warnning 所以只打印了以下三行
WARNING:root:warning警告信息
ERROR:root:error错误信息
CRITICAL:root:critical严重危险灾难信息
```
# Formatter  handler  logger 
#### Formatter
- 定义日志格式
- 可以根据实际需求定义不同的日志格式 
- 注意 这个和basicConfig的区别 这个不需要指定输出到那个文件和日志级别 会有专门干这两件事的代码
 ```
 import logging

formatter1=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p')

formatter2=logging.Formatter('%(asctime)s - %(module)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p'
 ```
 ```
 format常用格式说明
%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序名
%(funcName)s: 打印日志的当前函数
%(lineno)d: 打印日志的当前行号
%(asctime)s: 打印日志的时间
%(thread)d: 打印线程ID
%(threadName)s: 打印线程名称
%(process)d: 打印进程ID
%(message)s: 打印日志信息
 ```
 #### handler
-  定义日志输出到那个文件
- 分为两种
```
logging.FileHandler(file_path) 输出到文件
logging.StreamHandler()  输出到屏幕
```
```
fh1=logging.FileHandler("test1.log") #输出到文件
fh2=logging.FileHandler("test2.log")
ch=logging.StreamHandler() #输出到屏幕
```
#### logger
负责产生日志
```
logger1=logging.getLogger("landandan")  #拿到一个logger对象 默认是root 可以自定义
```
#### 三者之间的关系
![image](0B7DC5E610AA44D1B5522EAF1AE7C618)

# 封装好的logging模块
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang
"""
logging配置
"""

import os
import logging.config

# 定义三种日志输出格式 开始

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]' #其中name为getlogger指定的名字

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

# 定义日志绝对路径

logfile_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录

logfile_name = 'all2.log'  # log文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件 rorating 轮训 切割
            'formatter': 'standard',
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024*1024*5,  # 日志大小 5M 日志到了5M就自动切割
            'backupCount': 5, #日志保存几个
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}

def load_my_logging_cfg():
    logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
    #logger = logging.getLogger(__name__)  # 生成一个log实例
    #logger.info('It works!')  # 记录该文件的运行状态

if __name__ == '__main__':
    load_my_logging_cfg()
```
以上代码的使用方法如下：  
代码的所在的文件名字叫 my_logging.py   文件名字可以自定义 主要是导入文件   使用文件里的模块  
```
import logging
from my_logging import load_my_logging_cfg #导入文件 from 文件名 import 模块名 这种是在同级目录，不在同级目录的自己处理 目的是导入load_my_logging_cfg
load_my_logging_cfg() #执行导入的函数 这样会把logging的配置加载到现在的文件里

logger1=logging.getLogger(__name__) #拿到logger对象
#以上几行基本都是死的 不用变动
logger1.debug("debug") #写入日志信息
```