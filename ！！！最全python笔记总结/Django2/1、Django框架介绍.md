# 安装django
```
pip3 install django==2.2.9
pip3 show django
```
# 创建django项目
#### 命令行创建
```
# 创建项目
django-admin startproject mysite
# 创建功能模块app
cd mysite
python manage.py startapp app01
# 运行
python manage.py runserver 8001
```
#### pycharm创建
![image](D781A22AA99E407DB95E5E3BC22A1DCF)
#### 项目目录结构
```
mysite # 文件夹
    ├── app01 # 文件夹
    │   └── migrations # 文件夹
    │   └── admin.py
    │   └── apps.py
    │   └── models.py
    │   └── tests.py
    │   └── views.py
    ├── mysite # 文件夹
    │   └── settings.py
    │   └── urls.py
    │   └── wsgi.py
    └── templates # 文件夹
    ├── manage.py
# f关键文件介绍
-manage.py---项目入口,执行一些命令
-项目名
    -settings.py  全局配置信息
    -urls.py      总路由,请求地址跟视图函数的映射关系
-app名字
    -migrations   数据库迁移的记录
    -models.py    数据库表模型
    -views.py     处理业务逻辑的函数，简称视图函数
```
# Django简单示例
#### urls.py 路由
```
from django.contrib import admin
from django.urls import path,re_path # 导入re_path
#导入views模块
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    re_path(r'^index/$',views.index), # django2使用re_path匹配路径中的正则
]
```
#### views.py 视图
```
from django.shortcuts import render
# 必须定义一个request形参，request相当于我们自定义框架时的environ参数
def index(request):
    import datetime
    now=datetime.datetime.now()
    ctime=now.strftime("%Y-%m-%d %X")

    return render(request,"index.html",{"ctime":ctime}) # render会读取templates目录下的index.html文件的内容并且用字典中的ctime的值替换模版中的{{ ctime }}
```
#### templates 模板 index.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h4>当前时间:{{ ctime }}</h4>
</body>
</html>
```
# MVC模式和MTV模式
#### MVC
MVC，全名是Model View Controller 
```
M:Model模型负责业务对象与数据库的映射(ORM),用于数据库打交道  
V:view视图负责与用户的交互(html页面)  
C:Controller控制器接受用户的输入调用模型和视图完成用户的请求
```
  
#### MTV---django使用
MTV ，全名是 Model Template View
```
Model(模型)：负责业务对象与数据库的对象(ORM)  
Template(模版)：负责如何把页面展示给用户  
View(视图)：负责业务逻辑，并在适当的时候调用Model和Template

此外，Django还有一个urls分发器，它的作用是将一个个URL的页面请求分发给不同的view处理，
view再调用相应的Model和Template
```
# Django的生命请求周期
#### Django的分层
路由层（根据不同的地址执行不同的视图函数，详见urls.py）

视图层（定义处理业务逻辑的视图函数，详见views.py）

模型层 （跟数据库打交道的，详解models.py）

模板层（待返回给浏览器的html文件，详见templates）
#### 生命请求周期
![image](61BEE41D213E4FDD8FD234BA2B96336D)
