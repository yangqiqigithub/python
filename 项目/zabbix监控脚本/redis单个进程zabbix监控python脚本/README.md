### 使用方法
##### 安装redis模块
```
/usr/local/python3/bin/pip3 install redis
#如果上述方法安装不成功  按照下边的方法来
wget https://files.pythonhosted.org/packages/f5/00/5253aff5e747faf10d8ceb35fb5569b848cde2fdc13685d42fcf63118bbc/redis-3.0.1-py2.py3-none-any.whl  #自己寻找资源包
/usr/local/python3/bin/pip3 install redis-3.0.1-py2.py3-none-any.whl 
```
##### 配置zabbix-agent.conf文件
```
#redis6379 monitor
UserParameter=redis6379_connected_clients,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py  connected_clients
UserParameter=redis6379_connection_utilization,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py  connection_utilization
UserParameter=redis6379_rejected_connections,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py rejected_connections
UserParameter=redis6379_blocked_clients,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py blocked_clients
UserParameter=redis6379_used_memory,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py  used_memory
UserParameter=redis6379_memory_utilization,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py  memory_utilization
UserParameter=redis6379_used_memory_rss,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py  used_memory_rss
UserParameter=redis6379_mem_fragmentation_ratio,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py mem_fragmentation_ratio
UserParameter=redis6379_used_memory_peak,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py used_memory_peak
UserParameter=redis6379_used_memory_lua,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py used_memory_lua
UserParameter=redis6379_keyspace_hitrate,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py keyspace_hitrate
UserParameter=redis6379_latest_fork_usec,/usr/local/python3/bin/python3  /etc/zabbix/sh/redis/redis6379_info.py latest_fork_usec
```
##### 配置zabbix界面
对于浮点数 监控项里心里类型一定要是浮点数  不然就会类型不匹配  报错类似Value "2.59" of type "string" is not suitable for value type "Numeric (unsigned)"

监控项的名字和key的名字一样即可 ##对于浮点数 监控项里心里类型一定要是浮点数

触发器提示信息

```
redis6379_connection_utilization more  than 0.85   on{HOST.NAME}
redis6379_rejected_connections  more than 0   on{HOST.NAME}
redis6379_blocked_clients   more than 10   on{HOST.NAME}
redis6379_memory_utilization more than 0.85  on{HOST.NAME}
redis6379_mem_fragmentation_ratio  less than 1,memeory is too less  on{HOST.NAME}
redis6379_keyspace_hitrate less than 0.5   on{HOST.NAME}
```