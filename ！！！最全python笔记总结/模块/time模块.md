### 常用语法
```
import time

#时间戳
print(round(time.time()))#1543305923 
print(time.time()) #1543305922.7071424

#正常时间（格式化时间）
print(time.strftime("%Y-%m-%d %X")) #2018-11-27 16:05:22


#时间戳转化为 正常时间（格式化时间）
print(time.strftime("%Y-%m-%d %X",time.localtime(time.time()))) #2018-11-27 16:08:31
print(time.strftime("%Y-%m-%d %X",time.localtime(1543305922.7071424))) #2018-11-27 16:05:22

#正常时间（格式化时间）转化为时间戳
t=time.strftime("%Y-%m-%d %X")
print(t) #2018-11-27 16:08:10
print(time.mktime(time.strptime(t, '%Y-%m-%d %X'))) #1304584626.0
```
### 基础语法
在python里有三种方式表示时间：  
- 时间戳(timestamp)：通常来说，时间戳表示的是从1970年1月1日00:00:00开始按秒计算的偏移量。我们运行“type(time.time())”，返回的是float类型。
- 格式化的时间字符串(Format String)
- 结构化的时间(struct_time)：struct_time元组共有9个元素共九个元素:(年，月，日，时，分，秒，一年中第几周，一年中第几天，夏令时)
```
import time
print(time.time()) #1534918266.0805054 时间戳
print(time.localtime()) #本地时间 结构化时间 time.struct_time(tm_year=2018, tm_mon=8, tm_mday=22, tm_hour=14, tm_min=13, tm_sec=11, tm_wday=2, tm_yday=234, tm_isdst=0)
print(time.gmtime()) #utc时间 结构化时间 time.struct_time(tm_year=2018, tm_mon=8, tm_mday=22, tm_hour=6, tm_min=13, tm_sec=11, tm_wday=2, tm_yday=234, tm_isdst=0)
print(time.strftime("%Y-%m-%d %X")) # 2018-08-22 14:13:11 格式化时间
```
### 时间转换
![image](C27F3EC8376E4C68ABCAA22C5D67A1CD)
```
import time
#结构化时间 struct_time <=====> 格式化字符串时间 format string

#1> struct_time =====>
print(time.strftime('%Y-%m-%d %X', time.localtime()))
print(time.strftime('%Y-%m-%d %X', time.gmtime()))

#2>format string =====> struct_time
print(time.strptime('2011-05-05 16:37:06', '%Y-%m-%d %X'))

#结构化时间 struct_time <=====> 时间戳 timestamp

#1> timestamp ====> localtime
    #timestamp ====> gmtime
print(time.time())
print(time.localtime(1502330480.143894))
print(time.gmtime(1502330480.143894))

#2>  gmtime/localtime ======> timestamp
print(time.mktime(time.localtime()))
print(time.mktime(time.gmtime()))
 

import time
x=time.localtime()
print(x.tm_year)
print(x.tm_mon)
print(x.tm_mday)
print(x.tm_hour)
print(x.tm_min)
print(x.tm_sec)
'''
2018
8
22
14
39
15
'''
```
### linux相关时间
![image](6C28450BA90544679A3120C8E29BD19D)