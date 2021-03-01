from django.db import models
# Create your models here.
from rbac.models import UserInfo as RbacUserInfo
#区域表 例如北京四区
class area(models.Model):
    project_id=models.CharField(verbose_name='区域id',max_length=128,unique=True)
    project_name=models.CharField(verbose_name='区域英文名称',max_length=64,default=None)
    property_area=models.CharField(verbose_name='区域中文',max_length=64,default=None)
    account=models.ForeignKey('account',on_delete=models.Case)

#各个云平台的账号表
class account(models.Model):
    username=models.CharField(verbose_name='账号名称',max_length=32,default=None)
    platform = models.ForeignKey('platform', on_delete=models.Case)

#云平台表
class platform(models.Model):
    platname=models.CharField(verbose_name='平台名称',max_length=32,default=None)

#存放项目的表
class item(models.Model):
    itemname=models.CharField(verbose_name='项目名称',max_length=32,default=None)

#存放主机信息的表
class hosts(models.Model):
    host_id=models.CharField(verbose_name='主机id',max_length=128, unique=True)
    hostname=models.CharField(verbose_name='主机名称',max_length=64, default=None)
    pri_ip=models.CharField(verbose_name='主机内网IP',max_length=32, unique=True)
    pub_ip=models.CharField(verbose_name='主机公网IP',max_length=32, unique=True)
    status=models.CharField(verbose_name='状态',max_length=32, default=None)
    image_name=models.CharField(verbose_name='镜像名称',max_length=32, default=None)
    memory=models.IntegerField(verbose_name='内存大小',default=None)
    cpu=models.SmallIntegerField(verbose_name='cpu大小',default=None)
    ctime=models.DateTimeField(verbose_name='创建时间',default=None)
    volume_list=models.TextField(verbose_name='磁盘列表',default=None)
    area=models.ForeignKey('area',to_field='project_id',on_delete=models.Case)
    platform=models.ForeignKey('platform', on_delete=models.Case)
    account=models.ForeignKey('account', on_delete=models.Case)
    item=models.ForeignKey('item',on_delete=models.Case)

#存放数据库信息的表 由于数据库没那么多 Mysql Redis Mongo放在一张表中
class dbs(models.Model):
    db_id=models.CharField(verbose_name='数据库id',max_length=128, unique=True)
    dbname=models.CharField(verbose_name='数据库名称',max_length=64, default=None)
    type=models.CharField(verbose_name='数据库类型',max_length=32)
    mode=models.CharField(verbose_name='数据库架构类型',max_length=32)
    pri_ip=models.CharField(verbose_name='内网IP',max_length=32, unique=True)
    pub_ip=models.CharField(verbose_name='公网IP',max_length=32, default=None)
    status=models.CharField(verbose_name='状态',max_length=32, default=None)
    version=models.CharField(verbose_name='版本',max_length=32, default=None)
    memory=models.IntegerField(verbose_name='内存大小',default=None)
    cpu=models.CharField(verbose_name='cpu大小',max_length=32,default=None)
    ctime=models.DateTimeField(verbose_name='创建时间',default=None)
    disk=models.CharField(verbose_name='磁盘大小',max_length=32,default=None)
    area=models.ForeignKey('area',to_field='project_id',on_delete=models.Case)
    platform=models.ForeignKey('platform', on_delete=models.Case)
    account=models.ForeignKey('account', on_delete=models.Case)
    item=models.ForeignKey('item',on_delete=models.Case)





#部门表
class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=16)

    def __str__(self):
        return self.title


#用户表
class UserInfo(RbacUserInfo):
    """
    员工表
    """
    nickname = models.CharField(verbose_name='姓名', max_length=16)
    phone = models.CharField(verbose_name='手机号', max_length=32)

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, default=1)

    depart = models.ForeignKey(verbose_name='部门', to="Department",on_delete=models.Case)
    ctime =  models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.nickname




