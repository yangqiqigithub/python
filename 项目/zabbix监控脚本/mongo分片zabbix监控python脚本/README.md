### 使用方法
##### 创建mongo的监控用户
clusterMonitor: 为MongoDB Cloud Manager和Ops Manager监控代理工具提供只读访问权限。
```
use admin 
db.createUser(
   {
     user: "monitoruser",
     pwd: "123",
     roles: [ { role: "clusterMonitor", db: "admin" } ]
   }
 )
```
##### 模块安装
```
/usr/local/python3/bin/pip3  install pymongo
```
##### 配置zabbix-agent.conf文件
```
#mongo shard monitor
UserParameter=mongoshard_connects_current,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  connects_current
UserParameter=mongoshard_connects_utilization,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  connects_utilization
UserParameter=mongoshard_bytesIn,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  bytesIn
UserParameter=mongoshard_bytesOut,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  bytesOut
UserParameter=mongoshard_physicalBytesIn,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  physicalBytesIn
UserParameter=mongoshard_physicalBytesOut,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  physicalBytesOut
UserParameter=mongoshard_insert_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  insert_count
UserParameter=mongoshard_query_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  query_count
UserParameter=mongoshard_update_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  update_count
UserParameter=mongoshard_delete_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  delete_count
UserParameter=mongoshard_getmore_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  getmore_count
UserParameter=mongoshard_command_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  command_count
UserParameter=mongoshard_used_memeory,/usr/local/python3/bin/python3 /etc/zabbix/sh/mongo/mongoshard_serverstatus.py  used_memeory
```
##### 配置zabbix界面
对于浮点数 监控项里心里类型一定要是浮点数  不然就会类型不匹配  报错类似Value "2.59" of type "string" is not suitable for value type "Numeric (unsigned)"

监控项的名字和key的名字一样即可

触发器
```
mongoshard_connects_utilization more than 0.85 on {HOST.NAME}
```