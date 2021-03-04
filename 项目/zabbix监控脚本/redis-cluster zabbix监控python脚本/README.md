#### 模块安装
```
/usr/local/python3/bin/pip3 install redis-py-cluster
```
##### zabbix-agent.conf的配置
```
#redis cluster monitor
UserParameter=redis_cluster_state,/usr/local/python3/bin/python3 /etc/zabbix/sh/redis/redis_clusterinfo.py cluster_state
UserParameter=redis_cluster_slots_ok,/usr/local/python3/bin/python3 /etc/zabbix/sh/redis/redis_clusterinfo.py cluster_slots_ok
UserParameter=redis_cluster_slots_fail,/usr/local/python3/bin/python3 /etc/zabbix/sh/redis/redis_clusterinfo.py  cluster_slots_fail
UserParameter=redis_cluster_known_nodes,/usr/local/python3/bin/python3 /etc/zabbix/sh/redis/redis_clusterinfo.py  cluster_known_nodes
```
配置完毕重启agent
如果不是root用户建议 脚本放在宿主用户家目录下  
/etc/zabbix/sh/redis/redis_clusterinfo.py
##### zabbix界面的配置
监控项名字和key的名字一样即可

触发器提示信息
```
redis cluster_state is fail on {HOST.NAME}
redis cluster_slots_ok is not 16384  on {HOST.NAME}
redis cluster_slots_fail is not 0 on {HOST.NAME}
redis cluster_known_nodes is not 6  on {HOST.NAME}
```