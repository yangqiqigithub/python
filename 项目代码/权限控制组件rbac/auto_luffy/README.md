### 程序说明
web程序是通过 url 的切换来查看不同的页面（功能），所以权限指的其实就是URL，对url控制就是对权限的控制。
一个人有多少个权限就取决于他有多少个URL的访问权限。
程序中的rbac组件可以按照使用方法组合到自己的程序中


### 数据库建表逻辑
围绕用户表展开    
一个部门包含多个用户  
一个用户属于多个角色，一个角色里包含多个用户  
角色绑定权限，一个角色有多个权限，一个权限属于多个角色  
为了给权限再细分组，有了一级菜单和二级菜单
一级菜单里包含多个二级菜单，二级菜单里包含多个具体的权限（url）
在权限分配界面，用户绑定角色，角色绑定一级菜单，一级菜单下有二级菜单，二级菜单里有具体的权限，从而实现用户绑定了具体的权限

##### 部门表 app01_department

id | title
---|---
1 | 教学部
2 | 销售部
```
#app01/models.py
class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.title
## 部门和用户的关系：一对多
一个部门有多个用户，一个用户只能属于一个部门
```

##### 用户表 app01_userinfo
id | name | password | email | phone | level | depart_id
---|--- | --- | --- | --- | --- | ---
1 | qiqi | xxxx | 123@123.com | 12374550986 | 1 | 1
2 | gege | xxxx | 123@163.com | 12365789087 | 1 | 1
```
#app01/models.py
class UserInfo(RbacUserInfo):
    """
    用户表
    """
    phone = models.CharField(verbose_name='联系方式', max_length=32)
    level_choices = (
        (1, 'T1'),
        (2, 'T2'),
        (3, 'T3'),
    )
    level = models.IntegerField(verbose_name='级别', choices=level_choices)

    depart = models.ForeignKey(verbose_name='部门', to='Department')
#rbac/models.py
class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # django以后再做数据库迁移时，不再为UserInfo类创建相关的表以及表结构了。
        # 此类可以当做"父类"，被其他Model类继承。
        abstract = True
## 用户表有个继承关系
用户和部门的关系：一对多
一个部门有多个用户，一个用户只能属于一个部门
用户和角色的关系：多对多
一个用户有多个角色，一个角色可以属于多个用户
```
##### 角色表 rbac_roe
id | title
---|---
1 | CEO
2 | CTO
```
# rbac/models.py
class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title
## 角色和用户的关系：多对多
一个用户有多个角色，一个角色可以属于多个用户
角色和权限的关系：多对多
一个角色可以有多个权限，一个权限可以属于多个角色
```

##### 权限表 rbac_permission
id | title | url | name | menu_id | pid_id 
---|--- | --- | --- | --- | --- | ---
4 | 用户列表 | /user/list/ | user_list | 2 | null 
5 | 添加用户 | /user/add/ | user_add | null | 4
6 | 编辑用户 | /user/edit/(?P<pk>\d+)/ | user_edit | null | 4
7 | 删除用户 | /user/del/(?P<pk>\d+)/ | user_del | null  | 4
8 | 重置密码 | /user/reset/password/(?P<pk>\d+)/ | user_reset_pwd | null  | 4
18 | 添加一级菜单 | /rbac/menu/add/ | rbac:menu_add | null  | 17
19 | 编辑一级菜单 | /rbac/menu/edit/(?P<pk>\d+)/ | rbac:menu_edit | null | 17
20 | 删除一级菜单 | /rbac/menu/del/(?P<pk>\d+)/ | rbac:menu_del | null | 17
21 | 添加二级菜单 | /rbac/second/menu/add/(?P<menu_id>\d+) | rbac:second_menu_add | null | 17
22 | 编辑二级菜单 | /rbac/second/menu/edit/(?P<pk>\d+)/ | rbac:second_menu_edit | null  | 17
23 | 删除二级菜单 | /rbac/second/menu/del/(?P<pk>\d+)/ | rbac:second_menu_del | null  | 17
24 | 添加权限 | /rbac/permission/add/(?P<second_menu_id>\d+)/ | rbac:permission_add | null  | 17
25 | 编辑权限 | /rbac/permission/edit/(?P<pk>\d+)/ | rbac:permission_edit | null  | 17
26 | 删除权限 | /rbac/permission/del/(?P<pk>\d+)/ | rbac:permission_del | null  | 17
27 | 批量操作权限 | /rbac/multi/permissions/ | rbac:multi_permissions | null | 17
28 | 批量删除权限 | /rbac/multi/permissions/del/(?P<pk>\d+)/ | rbac:multi_permissions_del | null  | 17
29 | 权限分配 | /rbac/distribute/permissions/ | rbac:distribute_permissions | 1 | null

```
#rbac/models.py
class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)

    name = models.CharField(verbose_name='URL别名', max_length=32, unique=True)

    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True, blank=True, help_text='null表示不是菜单;非null表示是二级菜单')

    pid = models.ForeignKey(verbose_name='关联的权限', to='Permission', null=True, blank=True, related_name='parents',
                            help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单')

    def __str__(self):
        return self.title

## 权限表相对比较复杂，很重要
权限表包含的内容基本都展示在这个页面：/rbac/menu/list/，这个表的逻辑关系可以启动项目看着这个页面/rbac/menu/list/?mid=1&sid=13，会更加清晰
权限表每个字段的意思：
id
title 这里包含内容丰富，包含了一级菜单名称、二级菜单名称、以及二级菜单对应的权限名称
url
name 别名
menu_id 通过本表中的menu_id和id的对应关系，就能确定一级菜单包含哪些二级菜单
pid_id 通过本表中的pid_id和id的对应关系，就能确定二级菜单包含那些具体的权限
```

##### 菜单表
id | title |icon
---|---|---
1 | 权限管理 | fa-hourglass-3
2 | 用户管理 | fa-id-card-o
```
# rbac/models.py 一级菜单表
class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(verbose_name='菜单名称', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title
```