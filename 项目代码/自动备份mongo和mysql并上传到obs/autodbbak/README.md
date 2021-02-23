# 脚本功能
1、自动备份mysql和mongo    
2、自动清理过期的备份  
3、自动将备份文件上传到华为云上的obs  
# 程序说明：
```
	bin
		run.py 运行文件
			mongobak() 控制mongo的备份
			mysqlbak() 控制mysql的备份
	common
		common.py 放一些公用的函数
		obs_upload_file_mode.py 自动上传文件到obs的模块
	config 配置目录
		dbinfo.ini 配置数据库和obs的认证信息
	log 存放日志的目录
	Plugin
		mongobak.py 备份mongo的实体代码
		mysqlbak.py 备份mongo的实体代码
```
# 使用方法

### 安装python3的方法 
```
	yum -y install zlib*
    tar -xvJf Python-3.6.2.tar.xz
    cd Python-3.6.2
    ./configure  --prefix=/data/app/python3.6 --with-ssl
    make
    make install
```

### 安装obs模块
见华为云官方文档https://support.huaweicloud.com/sdk-python-devg-obs/zh-cn_topic_0142811715.html
### 配置config目录里的dbinfo.ini文件
```
;注意 ：
    ;以下所有的值，都是直接写即可，不要写单引号或者双引号


;填写obs相关信息
[obs_info]
ak = xxxxxxxxxxx
sk = xxxxxxxxxx
server = https://xxxxx
bucketname = xxxxxxxx


;填写mongo相关信息
[mongo_info]
host = 1.1.1.1
port = 8898
user = mybakuser
pwd = xxxxxx
obsdir_parent = bqj_mongodb_backup ;这里写啥，obs的备份目录就是啥  例如 /bqj_mongodb_backup/201908/20180807
mongo_cmd_path = /data/app/mongo3.4/bin/mongo
mongodump_cmd_path = /data/app/mongo3.4/bin/mongodump
bak_parent_path = /data/dbbackup/bqj/bqj_mongodb_backup/  这个路径一定要以/结尾,是服务器上的备份目录

;填写mysql相关信息
[mysql_info]
host = 1.1.1.1
port = 3306
user = mybakuser
pwd = xxxx
obsdir_parent = bqj_mysql_backup
mysql_cmd_path = /data/app/mysql5.6/bin/mysql
mysqldump_cmd_path = /data/app/mysql5.6/bin/mysqldump
bak_parent_path = /data/dbbackup/bqj/bqj_mysqldb_backup/这个路径一定要以/结尾 是服务器上的备份目录 
```
### 运行脚本
```
python3 bin/run.py
```

### 创建备份用户的方法：
```
    Mysql:
        grant SELECT,RELOAD,SHOW DATABASES,SHOW VIEW,show events,LOCK TABLES,EVENT,REPLICATION CLIENT,process,execute on *.* to 'mybackuser'@'10.64.34.%' identified by 'xxxx';
    Mongo:
        备份用户：
            use admin;
            db.createUser(
                {
                    user: "bakuser",
                    pwd: "123456",
                    roles: [ { role: "backup", db: "admin" } ]
                    }
                );
         恢复用户：
            use admin;
            db.createUser(
                {
                    user: "restoreuser",
                    pwd: "123456",
                    roles: [ { role: "restore", db: "admin" } ]
                    }
                );
```
                







