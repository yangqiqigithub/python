# 增
```
方式一：
models.UserInfo.objects.create(username='root',password='123')

方式二：
user_dic={
    'username':'zhaojie',
    'password':'999'
}
models.UserInfo.objects.create(**user_dic)

方式三：
obj=models.UserInfo(username='ALEX',password='566')
obj.save()
```
# 删
```
models.UserInfo.objects.filter(username='root').delete() 
```
# 改
```
models.UserInfo.objects.filter(id=2).update(password='000000')
```
# 查
### 查看所有
```
userobj_list=models.UserInfo.objects.all() 
print(userobj_list) 
'''
返回一个列表 一行是一个对象
<QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
'''
for row in userobj_list:
    print(row.id,row.username,row.password)
'''
    1 root 123
    2 ALEX 566
    3 zhaojie 999
'''
```
### 过滤
##### filter
```
obj=models.UserInfo.objects.filter(username='root') #过滤 <QuerySet [<UserInfo: UserInfo object (1)>]>
obj=models.UserInfo.objects.filter(username='root') #过滤 <QuerySet [<UserInfo: UserInfo object (1)>]>
```
##### values和values_list
```
v=models.Business.objects.all()
v2=models.Business.objects.all().values('id','caption')
v3=models.Business.objects.all().values_list('id','caption')
#print(v,v2,v3) #QuerySet 三个都是
for i in v:
    print(i) #
    '''
    一个个对象
    Business object (1)
    Business object (2)
    Business object (3)
    Business object (4)
    
    '''

for i2 in v2:
    print(i2)
    '''
    一个个字典
    {'id': 1, 'caption': '运维部'}
    {'id': 2, 'caption': '开发'}
    {'id': 3, 'caption': '市场'}
    {'id': 4, 'caption': '测试'}
    '''

for i3 in v3:
    print(v3)
    '''
    一个个Queryset 里边是元组
    <QuerySet [(1, '运维部'), (2, '开发'), (3, '市场'), (4, '测试')]>
    <QuerySet [(1, '运维部'), (2, '开发'), (3, '市场'), (4, '测试')]>
    <QuerySet [(1, '运维部'), (2, '开发'), (3, '市场'), (4, '测试')]>
    <QuerySet [(1, '运维部'), (2, '开发'), (3, '市场'), (4, '测试')]>
```
##### only
```
models.UserInfo.objects.only('id','pwd')
<QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>, <UserInfo: UserInfo object (4)>]>
拿出筛选出来的queryset
```
##### defer
```
models.UserInfo.objects.defer('id','pwd')
<QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>, <UserInfo: UserInfo object (4)>]>
拿出除了条件上的queryset，和only相反
```
##### exclude 
```
# 排除
models.UserInfo.objects.exclude(id=1)
<QuerySet [<UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
```
##### 排序
```
models.UserInfo.objects.all().order_by('id') #默认从小到大
models.UserInfo.objects.all().order_by('-id') #从大到小
	<QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>, <UserInfo: UserInfo object (4)>]>
```
### 正向和反向查询
表结构
```
class UserType(models.Model):
    name=models.CharField(max_length=32)
    
class User(models.Model):
    user=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    ut=models.ForeignKey(to='UserType',to_field='id',on_delete=None)
```
##### 正向查找
```
v = User.objects.all()
for item in v:
     item.user
     item.pwd
     item.ut.name #item.ut拿到的关联表的一条数据，一个对象
User.objects.all().values('user','ut__name') #跨表查询
```
##### 反向查找
```
v = models.UserType.objects.all()
for item in v:
    # print(item.name)
    print(item.user_set) #app01.User.None 拿到的是整个表，并不是一条数据
    print(item.user_set.all())
        '''
        <QuerySet [<User: User object (1)>, <User: User object (4)>]>
        <QuerySet [<User: User object (2)>]>
        <QuerySet [<User: User object (3)>]>
        '''
# models.UserType.objects.all().values('name','user__pwd')

反向操作时，使用的字段名，用于代替 【表名_set】 如： obj.表名_set.all()
 related_name=None,   
 反向操作时，使用的连接前缀，用于替换【表名】         
related_query_name=None,    
如： models.UserGroup.objects.filter(表名__字段名=1).values('表名__字段名')
```
### 神奇的双下划线
```
#views.py
def hosts(request):
    hosts=models.Host.objects.all()
    hosts1=models.Host.objects.all().values('hostname','b__caption') 
    #对于这种格式 包括values_list() 这种选取固定字段的都用双下划线

    return render(request,'hosts.html',{'hosts':hosts,'hosts1':hosts1})

#hosts.html
<table border="1px">
    <tr>
        <td>id</td>
        <td>主机名</td>
        <td>IP</td>
        <td>端口</td>
        <td>业务</td>
    </tr>
    {% for host in hosts %}
        <tr host-id="{{ host.nid }}">
            <td>{{ forloop.counter }}</td>
            <td>{{ host.hostname }}</td>
            <td>{{ host.ip }}</td>
            <td>{{ host.port }}</td>
            <td>{{ host.b.caption }}</td> #对于这种全部拿出的就用点
        </tr>

    {% endfor %}

</table>

<table border="1px">
    <tr>
        <td>id</td>
        <td>主机名</td>
        <td>业务</td>
    </tr>
    {% for host1 in hosts1 %}
        <tr>
            <td>{{ forloop.counter }}</td>
            <td>{{ host1.hostname }}</td>
            <td>{{ host1.b__caption }}</td> #对于这种通过values选择指定字段的就用双下划线，并且写b__caption
        </tr>
    {% endfor %}

</table>
```
# 性能优化
select_related 
原理：进行join连表操作
```
				
users = models.User.objects.all().select_related('ut')
for row in users:
	print(row.user,row.pwd,row.ut_id)
	print(row.ut.name)
	print(row.tu.name) # 再发起一次SQL请求
```				
prefetch_related
#不发生连表操作，原表发送一次请求，连接的表单独再发送请求
```
users = models.User.objects.filter(id__gt=30).prefetch_related('ut','tu')
# select * from users where id > 30
#获取上一步骤中所有的ut_id=[1,2]
# select * from user_type where id in [1,2]
# select * from user_type where id in [1,2]
					
for row in users:
	print(row.user,row.pwd,row.ut_id)
	print(row.ut.name)
```