```
import datetime

print(datetime.datetime.now()) #2018-08-22 14:44:10.795668 当前时间
print(datetime.date.fromtimestamp(time.time())) #2018-08-22 时间戳直接转换成格式化时间
print(datetime.datetime.now()+datetime.timedelta(3)) #2018-08-25 14:47:16.946314 后三天
print(datetime.datetime.now()+datetime.timedelta(-3)) # 2018-11-24 16:18:58.307905 前三天
```