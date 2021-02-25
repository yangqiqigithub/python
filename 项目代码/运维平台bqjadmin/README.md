# 程序结构
autoclient  客户端--负责采集服务器信息  
bqjadmin    服务端

# autoclient客户端介绍
### 程序结构说明
```
bin 
    get_appmoni.py 按照指定的服务（nginx、mysql...）收集服务监控项的信息
    get_serverinfo.py  获取服务器的基本配置数据
    get_servermoni.py  获取服务器的硬件使用情况信息
config 
    settings 配置日志路径、指定监控哪些服务、指定信息上报接口
core 核心代码目录
    base.py 基类，封装基础方法
    appmonitor.py  获取服务监控数据代码
    serverinfo.py  获取服务器基础配置数据的代码
    servermonitor.py  获取服务器硬件使用情况数据的代码
    client.py  定义本地标示和上报信息的方式
lib  存放公共使用的函数
    common.py
    log.py
    response.py
    serialize.py
log 日志存放目录    
```
### 使用方法
在系统设置定时任务，定时像settings里设置的接口上报数据，服务端接收到数据后会
进行数据校验并写入数据库
```
python3 ./bin/get_appmoni.py
python3 ./bin/get_serverinfo.py
python3 ./bin/get_servermoni.py
```
可以会用ansible将客户端批量部署到系统上
# bqjadmin服务端介绍
### 程序结构说明
```
api 专门用来处理客户端数据，负责接收客户端数据并校验入库
    models.py 定义数据库和表
    urls.py 定义客户端上报数据的路由
    views.py 处理客户端上报的数据并入库
bqjadmin 配置
    settings.py 总配置
    urls.py 总路由
cmdb 程序主要功能
    utils 工具包
    views 核心代码目录
        account.py 处理用户和用户组的展示、编辑、删除
        show_hosts.py 处理主机的展示、模糊和组合搜索、排序、分页等等
rbac 专门单独出来处理权限问题的
    用户绑定角色，不同的角色对应不同的策略，不同的策略绑定不同的路径，
    从而实现不同的用户访问不同的路径也就是有不同的权限
```