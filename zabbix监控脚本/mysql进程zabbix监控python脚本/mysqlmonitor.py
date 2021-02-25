#!/usr/local/python3/bin/python3
# -*- coding: utf-8 -*-
# Author qiqiYang


import  pymysql
import sys

connect = pymysql.connect(host='192.168.50.216',
                           user='monitor',
                           password='monitor',
                           db='mysql',
                           port=3306,
                           charset='utf8')
cursor = connect.cursor()
#cursor.execute('show processlist')


cursor.execute('show global status')
result = cursor.fetchall()
status_dict={}
for i in result:
    #print(i[0],i[1])
    status_dict.setdefault(i[0],i[1])


def mysql_monitor(sysargv1):
    uptime=int(status_dict['Uptime'])

    #TPS 数据库每秒执行的事务数
    commit_count=int(status_dict['Com_commit'])
    rollback_count=int(status_dict['Com_rollback'])
    tps=round((commit_count+rollback_count)/uptime,2)


    #QPS 数据库每秒执行的SQL数
    select_count=int(status_dict['Com_select'])
    insert_count=int(status_dict['Com_insert'])
    delete_count=int(status_dict['Com_delete'])
    update_count=int(status_dict['Com_update'])
    sql_count=select_count+insert_count+delete_count+update_count
    qps=round(sql_count/uptime,2)

    # select 每秒执行的次数
    select_persec_count=round(select_count/uptime)
    # update 每秒执行的次数
    update_persec_count=round(update_count/uptime)
    # delete 每秒执行的次数
    delete_persec_count=round(delete_count/uptime)
    # insert 每秒执行的次数
    insert_persec_count=round(insert_count/uptime)
    # rollback 每秒执行的次数
    rollback_persec_count=round(rollback_count/uptime)
    # commit 每秒执行的次数
    commit_persec_count=round(commit_count/uptime)

    #mysql当前连接数
    threads_connects=int(status_dict['Threads_connected'])

    #mysql连接数使用率 低于0.85 报警
    cursor.execute("show variables like 'max_connections';")
    max_connects=int(cursor.fetchall()[0][1])
    thread_connects_rate=round(threads_connects/max_connects,2)

    #mysql当前打开文件数
    openfiles=int(status_dict['Open_files'])

    #mysql打开文件数使用率
    cursor.execute("show variables like 'open_files_limit';")
    openfiles_limit=int(cursor.fetchall()[0][1])
    openfiles_rate=round(openfiles_limit/openfiles,2)

    #在磁盘上每秒创建临时表的数量  内存无法放下的时候才会在磁盘创建  大于5就报警
    created_tmp_disk_tables_count=round(int(status_dict['Created_tmp_disk_tables'])/uptime,5)

    #在内存中每秒创建临时表的数量
    created_tmp_memory_tables_count=round(int(status_dict['Created_tmp_tables'])/uptime,2)

    #表扫描率  超过4000 就 报警
    scan_table_rate=round(int(status_dict['Handler_read_rnd_next'])/int(status_dict['Com_select']),2)

    #慢查询每分钟的数量  超过4个就报警
    slow_queries_permin_count=int(status_dict['Slow_queries'])/uptime/60
    #print(slow_queries_permin_count)

    #Innodb从物理磁盘每秒读出的数据量大小  M
    innodb_data_read_size=round(int(status_dict['Innodb_data_read'])/1024/1024/uptime,4)

    #Innodb从物理磁盘每秒写入的数据量大小  M
    innodb_data_write_size=round(int(status_dict['Innodb_data_written'])/1024/1024/uptime,4)

    #Innodb从物理磁盘每秒读出的数据的次数
    innodb_data_read_count=round(int(status_dict['Innodb_data_reads'])/uptime,4)

    #Innodb从物理磁盘每秒写入的数据的次数
    innodb_data_write_count=round(int(status_dict['Innodb_data_writes'])/uptime,4)

    #每秒钟mysql实例接受的查询次数 不仅仅是select
    queries_persec_count=round(int(status_dict['Queries'])/uptime,2)

    #mysql实例每秒钟接收的流量
    mysql_persec_receive_size=round(int(status_dict['Bytes_received'])/1024/1024/uptime,4)

    #mysql实例每秒钟发送的流量
    mysql_persec_send_size=round(int(status_dict['Bytes_sent'])/1024/1024/uptime,4)


    #以下监控项要求开启 query_cache_size 缓存 默认是0  否则以下监控作废
    #查询缓存命中率  低于0.85 报警
    #select_cache_hitrate=round((int(status_dict['Qcache_hits']))/int(status_dict['Qcache_hits']),2)

    #查询缓存使用率
    # cursor.execute("show variables like 'query_cache_size%';")
    # query_cache_size=int(cursor.fetchall()[0][1])
    # qcache_free_memory=int(status_dict['Qcache_free_memory'])/1024/1024
    # select_cache_rate=(query_cache_size - qcache_free_memory) / query_cache_size


    if sys.argv[1]=='tps':
        print(tps)
    elif sys.argv[1]=='qps':
        print(qps)
    elif sys.argv[1]=='select_persec_count':
        print(select_persec_count)
    elif sys.argv[1]=='update_persec_count':
        print(update_persec_count)
    elif sys.argv[1]=='delete_persec_count':
        print(delete_persec_count)
    elif sys.argv[1]=='insert_persec_count':
        print(insert_persec_count)
    elif sys.argv[1]=='rollback_persec_count':
        print(rollback_persec_count)
    elif sys.argv[1]=='commit_persec_count':
        print(commit_persec_count)
    elif sys.argv[1]=='threads_connects':
        print(threads_connects)
    elif sys.argv[1]=='thread_connects_rate':
        print(thread_connects_rate)
    elif sys.argv[1]=='openfiles':
        print(openfiles)
    elif sys.argv[1]=='openfiles_rate':
        print(openfiles_rate)
    elif sys.argv[1]=='created_tmp_disk_tables_count':
        print(created_tmp_disk_tables_count)
    elif sys.argv[1]=='created_tmp_memory_tables_count':
        print(created_tmp_memory_tables_count)
    elif sys.argv[1]=='scan_table_rate':
        print(scan_table_rate)
    elif sys.argv[1]=='slow_queries_permin_count':
        print(slow_queries_permin_count)
    elif sys.argv[1]=='innodb_data_read_size':
        print(innodb_data_read_size)
    elif sys.argv[1]=='innodb_data_write_size':
        print(innodb_data_write_size)
    elif sys.argv[1]=='innodb_data_read_count':
        print(innodb_data_read_count)
    elif sys.argv[1]=='innodb_data_write_count':
        print(innodb_data_write_count)
    elif sys.argv[1]=='queries_persec_count':
        print(queries_persec_count)
    elif sys.argv[1]=='mysql_persec_receive_size':
        print(mysql_persec_receive_size)
    elif sys.argv[1]=='mysql_persec_send_size':
        print(mysql_persec_send_size)
    # elif sys.argv[1]=='select_cache_hitrate':
    #     print(select_cache_hitrate)
    # elif sys.argv[1]=='select_cache_rate':
    #     print(select_cache_rate)

    else:
        pass

mysql_monitor(sys.argv[1])






