# 创建表
```
#models.py
class Employee(models.Model):  # 必须是models.Model的子类
    id=models.AutoField(primary_key=True)

    name=models.CharField(max_length=16)

    gender=models.BooleanField(default=1)

    birth=models.DateField()

    department=models.CharField(max_length=30)

    salary=models.DecimalField(max_digits=10,decimal_places=1)
```
# 配置settings.py
#### 注册应用
 但凡涉及到数据库同步操作的应用，都需要事先在settings.py的INSTALLED_APPS中完成注册
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django2.x+版本
    'app01.apps.App01Config', # 如果默认已经添加了，则无需重复添加
    # 'app02.apps.App02Config', # 若有新增的app，按照规律依次添加即可

    # django1.x版本
    'app01',  # 直接写应用名字
    # 'app02'
]
```
#### 配置后端数据库
django的orm支持多种数据库（如PostgreSQL、MySQL、SQLite、Oracle等），如果想将上述模型转为mysql数据库中的表，需要settings.py中配置DATABASES，如下
```
# 删除\注释掉原来的DATABASES配置项，新增下述配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 使用mysql数据库
        'NAME': 'db1',          # 要连接的数据库,需要提前创建好
        'USER': 'root',         # 链接数据库的用于名
        'PASSWORD': '',         # 链接数据库的用于名                  
        'HOST': '127.0.0.1',    # mysql服务监听的ip  
        'PORT': 3306,           # mysql服务监听的端口  
        'ATOMIC_REQUEST': True, #设置为True代表同一个http请求所对应的所有sql都放在一个事务中执行 
                                #(要么所有都成功，要么所有都失败)，这是全局性的配置，如果要对某个
                                #http请求放水（然后自定义事务），可以用non_atomic_requests修饰器 
        'OPTIONS': {
            "init_command": "SET storage_engine=INNODB", #设置创建表的存储引擎为INNODB
        }
    }
}
# django2使用mysql需要安装mysqlclient模块
pip install mysqlclient
```
#### 配置日志
如果想打印orm转换过程中的sql，需要在settings中进行配置日志
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}
```
#### 数据库迁移命令
```
$ python manage.py makemigrations
$ python manage.py migrate
```
# 表字段Fields
#### 字段类型
```
#1、AutoField
int自增列，必须填入参数 primary_key=True。当model中如果没有自增列，则自动会创建一个列名为id的列。

#2、IntegerField
一个整数类型,范围在 -2147483648 to 2147483647。

#3、CharField
字符类型，必须提供max_length参数， max_length表示字符长度。

#4、DateField
日期字段，日期格式  YYYY-MM-DD，相当于Python中的datetime.date()实例。

#5、DateTimeField
日期时间字段，格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]，相当于Python中的datetime.datetime()实例
```
示例
```
class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```
#### 字段选项/参数
每个字段都有一组特定于该字段的参数。例如字段CharField（及其子类）必须定义一个max_length参数，该参数指定用于存储数据的VARCHAR数据库字段的大小
```
null：如果为True，Django将在数据库中将空值存储为NULL。默认值为False。
blank：如果为True，则该字段允许为空。默认值为False。

unique: 如果为True，该字段必须是唯一的

db_index 如果db_index=True 则代表着为此字段设置索引。

choices
用于指定一个二元组，如果给定了此选项，则admin界面默认表单小部件将是一个选择框，而不是标准文本字段，并且将选择限制为给定的选项
from django.db import models
class Person(models.Model):
    # 每个元组的第二个元素用来在amdin管理界面显示，而第一个元素才是被存入数据库中的值
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
'L'
>>> p.get_shirt_size_display() # 可以使用这种方法访问具有选项的字段的显示值
'Large'



default 字段的默认值。这可以是值或可调用对象。如果可调用，则每次创建新对象时都将调用它。
from django.db import models
def func():
    print('from func')
class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60,null=True,default=func)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
# 首先我们设置null=True，default=函数
# 然后执行，当插入值为空时，会使用默认值，如果此时默认值为函数，则会触发函数的执行
>>> p = Person()
from func
>>> p.save()


auto_now_add
针对 DateField和DateTimeField可以设置auto_now_add=True，新增对象时会自动添加当前时间
create_time=models.DateTimeField(auto_now_add=True) # 只针对创建，不针对修改


auto_now
针对 DateField和DateTimeField可以设置auto_now=True，新增或修改对象都会自动填充当前时间
modify_time=models.DateTimeField(auto_now=True) # 针对创建以及修改都有效
选项auto_now、auto_now_add和default是互斥的,只能有一个


help_text, 用于在admin管理界面显示的额外“帮助”文本。它对于文档很有用 name = models.CharField(max_length=60,null=True,default=func,help_text='哈哈哈哈哈')


primary_key 如果为True，那么这个字段就是模型的主键 id = models.AutoField(primary_key=True)


针对ForeignKey、ManyToManyField和OneToOneField字段，第一个参数必须为模型类，如果要设置字段显示的详细名字，需要指定参数verbose_name，如下
from django.db import models
class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField('用户名',max_length=60,null=True,help_text='哈哈哈')
    role=models.ForeignKey(to='Role',verbose_name='权限选择',on_delete=models.CASCADE,null=True)
class Role(models.Model):
    PRIVS = (
        (0, 'superuser'),
        (1, 'user'),
        (2, 'visitor'),
    )
    role=models.CharField('角色',max_length=20)
    priv=models.IntegerField('权限',choices=PRIVS)
```
# 表关系
#### 一对多
外键建立在多的表里    
字段名字=models.ForeignKey('目标表',to_field='目标字段',on_delete=删除操作)   
django2.x必须添加删除操作  
```
# models.py
from django.db import models

class UserInfo(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=64)
    usergroup=models.ForeignKey('UserGroup',to_field='id',on_delete=models.SET,default=1)
    #创建完毕后usergroup在表里的字段名字叫做 usergroup_id,usergroup_id这个才是字段名字
    #而usergroup代表的是UserGroup这张表的一个对象 是一个对象

class UserGroup(models.Model):
    caption=models.CharField(max_length=32,unique=True)
    ctime=models.DateTimeField(auto_now_add=True)
    utime=models.DateTimeField(auto_now=True)
```
#### 多对多
1、自动创建关系表
```
class Host(models.Model):
	nid = models.AutoField(primary_key=True)
	hostname = models.CharField(max_length=32,db_index=True)
	ip = models.GenericIPAddressField(protocol="ipv4",db_index=True)
	port = models.IntegerField()
	b = models.ForeignKey(to="Business", to_field='id')

class Application(models.Model):
	name = models.CharField(max_length=32)
	r = models.ManyToManyField("Host")
				
上述两张表会自动创建第三张表 如下图：
只会创建固定的三个字段，不能再自己添加字段了
无法直接对第三张表进行操作
但是可以间接操作

obj = Application.objects.get(id=1)
#拿到一个id=1的Application表的对象
obj.name
			
# 第三张表操作
添加数据：
obj.r.add(1) 
obj.r.add(2)
obj.r.add(2,3,4)
obj.r.add(*[1,2,3,4]

#remove的原理和下文详细举例的add的原理一样
obj.r.remove(1)
obj.r.remove(2,4)
obj.r.remove(*[1,2,3])
			
obj.r.clear() #清空
			
obj.r.set([3,5,7])
#先清空所有和obj关联的，最后设置和obj关联
的关系只有 [3,5,7]
			
# 所有相关的主机对象“列表” QuerySet
obj.r.all()
```
			
2、自定义关系表，自定义第三张
```
class Host(models.Model):
	nid = models.AutoField(primary_key=True)
	hostname = models.CharField(max_length=32,db_index=True)
	ip = models.GenericIPAddressField(protocol="ipv4",db_index=True)
	port = models.IntegerField()
	b = models.ForeignKey(to="Business", to_field='id')

class Application(models.Model):
	name = models.CharField(max_length=32)

class HostToApp(models.Model):
	hobj = models.ForeignKey(to='Host',to_field='nid')
	aobj = models.ForeignKey(to='Application',to_field='id')
	
HostToApp.objects.create(hobj_id=1,aobj_id=2) 这种的就直接对第三张表进行操作
```
# META选项
在模型类内部定义Meta类（可选的，所有选项都不是必须的），可以配置模型的元数据，如排序选项（ordering），数据库表名（db_table）或者人类可读的单复数名称（verbose_name 和verbose_name_plural）
```
from django.db import models


class Person(models.Model):
    PRIORITY_CHOICES = [
        (0,'admin'),
        (1,'user'),
        (2,'visitor'),
    ]

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30,null=True)
    priority=models.IntegerField(choices=PRIORITY_CHOICES)
    create_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        # 数据库中生成的表名称 默认 app名称 + 下划线 + 类名
        db_table='my_table'

        # 联合索引
        index_together = [
            ("priority", "create_time"),
        ]

        # 建立联合索引推荐使用下面这种
        indexes = [
            models.Index(fields=["priority", "create_time"]), # 联合索引
            models.Index(fields=['priority'], name='priority_idx'), # 单独的索引
            # 关于索引名称：如果没有提供name，Django将自动生成一个索引名称。 为了兼容不同的数据库，索引名称不能超过30个字符，不能以数字（0-9）或下划线（_）开头。
        ]

        # 联合唯一索引
        unique_together = (("name", "priority"),)

        # 执行Person.objects.all()
        # 会先按照权限priority字段降序排，权限相同则按照创建时间create_time字段升序排
        ordering = ('-priority','create_time') 

        # admin中显示的表名称
        verbose_name = '哈哈哈'

        # verbose_name加s
        verbose_name_plural = verbose_name



        # 执行Person.objects.latest()
        # 会先按照权限priority字段降序排列，权限相同则按照id字段升序排列，然后取最后一个
        get_latest_by=['-priority','id'] 


    def __str__(self):
        return '%s:%s:%s' %(self.name,self.priority,self.create_time)
```
# 执行原生sql
raw()方法执行原生sql
```
ret=models.Book.objects.raw('select * from app01_book')
```