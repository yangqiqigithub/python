### 使用方法
##### 在mysql里创建监控用户
```
grant select,process,replication client on *.* to 'checkuser'@'%' identified by 'Qn@9865321';
flush privileges;
```
##### 模块安装
```
/usr/local/python3/bin/pip3 install  pymysql 
```
##### 配置zabbix-agent.conf
```
#mysql monitor
UserParameter=mysql_tps,usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py    tps
UserParameter=mysql_qps,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   qps
UserParameter=mysql_select_persec_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   select_persec_count
UserParameter=mysql_update_persec_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   update_persec_count
UserParameter=mysql_delete_persec_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   delete_persec_count
UserParameter=mysql_insert_persec_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   insert_persec_count
UserParameter=mysql_rollback_persec_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   rollback_persec_count
UserParameter=mysql_commit_persec_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   commit_persec_count
UserParameter=mysql_threads_connects,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   threads_connects
UserParameter=mysql_thread_connects_rate,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   thread_connects_rate
UserParameter=mysql_openfiles_rate,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   openfiles_rate
UserParameter=mysql_created_tmp_disk_tables_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   created_tmp_disk_tables_count
UserParameter=mysql_created_tmp_memory_tables_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   created_tmp_memory_tables_count
UserParameter=mysql_scan_table_rate,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   scan_table_rate
UserParameter=mysql_slow_queries_permin_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py  slow_queries_permin_count 
UserParameter=mysql_innodb_data_read_size,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   innodb_data_read_size
UserParameter=mysql_innodb_write_read_size,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   innodb_write_read_size
UserParameter=mysql_innodb_data_read_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   innodb_data_read_count
UserParameter=mysql_innodb_data_write_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   innodb_data_write_count
UserParameter=mysql_queries_persec_count,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   queries_persec_count
UserParameter=mysql_mysql_persec_receive_size,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   mysql_persec_receive_size
UserParameter=mysql_mysql_persec_send_size,/usr/local/python3/bin/python3 /etc/zabbix/sh/mysql/mysqlmonitor.py   mysql_persec_send_size
```
##### 配置zabbix界面
监控项和key的名字配置成一样的就行
```
mysql_created_tmp_disk_tables_count more than 5 on {HOST.NAME}	
mysql_scan_table_rate more than 4000 on {HOST.NAME}	
mysql_slow_queries_permin_count more than 3 per min on {HOST.NAME}	
mysql_thread_connects_rate more than 0.85 on {HOST.NAME}
```