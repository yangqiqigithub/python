# 使用方法
##### 1.导入模块
```
from xxx.record_log import Logger
```
##### 2. 实例化对象写入日志
```
Logger().log('我是运行日志') #默认写入运行日志文件run.log
Logger().log('我是错误日志',mode=False) #mode=False 写入错误日志文件 error.log
```	

##### 3. 日志内容大概如下：
```
error.log
    2017-02-22 18:10:43,275  - ERROR :  API授权失败
run.log
    2017-02-22 16:46:31,255 - INFO :  Success
```
#### 4. 日志文件路径的规划化
这里我把日志文件的路径规划直接写在了这个py文件里，但是对于一个项目而言，这种路径一般还在settings.py文件里规划好
.py参考配置：
```
import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 错误日志
ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')
```

在settings.py里设置好后，应该在此文件中导入，导入方式参考配置：
```
from config import settings

class Logger(object):
    __instance = None

    def __init__(self):
        self.run_log_file = settings.RUN_LOG_FILE #这里也应该修改成导入的路径
        self.error_log_file = settings.ERROR_LOG_FILE

然后此文件中的以下几行删除或者注释即可
BASEDIR = os.path.dirname(os.path.abspath(__file__))
错误日志
ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')
```

