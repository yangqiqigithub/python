# 路由层的作用
路由是请求地址和视图函数的映射关系，用户访问某个路径，会匹配路由配置里的路径，从而执行视图层相应的函数
# 示例及注意事项
### 示例展示
##### urls.py
```
#django2.x
from django.contrib import admin
from django.urls import path, re_path 
from app01 import views 
urlpatterns = [
    path('admin/', admin.site.urls), 
    re_path(r'^index/$',views.index), 
]

# django1.x
from django.conf.urls import url, 
from django.contrib import admin
from app01 import views 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
```
##### views.py
```
from django.shortcuts import render
from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse('index page...')
```
### 注意事项
```
1、django1.x中的url和django2.x中的re_path用法一样，可以匹配正则
2、urls.py里的路径，路径前不用加/,应该是^index而不是^/index
3、正则表达式前面的'r' 是可选的但是建议加上
4、如果想匹配的路径就只是index/,那么正则表达式应该有开始符与结束符, 如 ^index/$，这样逻辑才算严谨

5、http://127.0.0.1:8001/index/路径的匹配流程：
Django会拿着路径部分index/去路由表中自上而下匹配正则表达式，一旦匹配成功，则立即执行其后的视图函数，不会继续往下匹配，此处匹配成功的正则表达式是 r'^index/$'。

http://127.0.0.1:8001/index路径的匹配流程：
Django同样会拿着路径部分index去路由表中自上而下匹配正则表达式，貌似并不会匹配成功任何正则表达式（ r'^index/$'匹配的是必须以 / 结尾，所以不会匹配成功index），但实际上仍然会看到结果 index page...

原因如下：
在配置文件settings.py中有一个参数APPEND_SLASH，该参数有两个值True或False

当APPEND_SLASH=True（如果配置文件中没有该配置，APPEND_SLASH的默认值为True），并且用户请求的url地址的路径部分不是以 / 结尾，例如请求的url地址是 http://127.0.0.1:8001/index，Django会拿着路径部分（即index）去路由表中匹配正则表达式，发现匹配不成功，那么Django会在路径后加 / （即index/）再去路由表中匹配，如果匹配失败则会返回路径未找到，如果匹配成功，则会返回重定向信息给浏览器，要求浏览器重新向 http://127.0.0.1:8001/index/地址发送请求。
当APPEND_SLASH=False时，则不会执行上述过程，即一旦url地址的路径部分匹配失败就立即返回路径未找到，不会做任何的附加操作
```
# 分组
### 普通分组
##### urls.py
```
from django.contrib import admin
from django.urls import path,re_path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 下述正则表达式会匹配url地址的路径部分为:article/数字/，匹配成功的分组部分会以位置参数的形式传给视图函数，有几个分组就传几个位置参数
    re_path(r'^article/(\d+)/$',views.article), 
]
```
##### views.py
```
from django.shortcuts import render
from django.shortcuts import HttpResponse

# 需要额外增加一个形参用于接收传递过来的分组数据
def article(request,article_id):
    return HttpResponse('id为 %s 的文章内容...' %article_id)
```
### 命名分组
命名分组按照key=value的形式传参
##### urls.py
```
from django.contrib import admin
from django.urls import path,re_path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 该正则会匹配url地址的路径部分为:article/数字/，匹配成功的分组部分会以关键字参数（article_id=匹配成功的数字）的形式传给视图函数，有几个有名分组就会传几个关键字参数，需要强调一点是：视图函数得到的值均为字符串类型
    re_path(r'^article/(?P<article_id>\d+)/$',views.article), 
]
```
##### views.py
```
from django.shortcuts import render
from django.shortcuts import HttpResponse

# 需要额外增加一个形参，形参名必须为article_id
def article(request,article_id):
    return HttpResponse('id为 %s 的文章内容...' %article_id)
```
*==普通分组和命名分组不要混合使用==*
# 路由分发
```
from django.contrib import admin
from django.urls import path,re_path,include

# 总路由表
urlpatterns = [
    path('admin/', admin.site.urls),

    # 新增两条路由，注意不能以$结尾
    # include函数就是做分发操作的，当在浏览器输入http://127.0.0.1:8001/app01/index/时，会先进入到总路由表中进行匹配，正则表达式r'^app01/'会先匹配成功路径app01/，然后include功能会去app01下的urls.py中继续匹配剩余的路径部分
    re_path(r'^app01/', include('app01.urls')),
    re_path(r'^app02/', include('app02.urls')),
]
```
# 反向解析
给url起个别名，如果以后路径变了，但是根据别名还可以找到修改后的路劲，避免代码大规模修改
### 示例：登录成功跳转到index页面
##### urls.py
```
from django.contrib import admin
from django.urls import path,re_path
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^login/$', views.login,name='login_page'), # 路径login/的别名为login_page
    re_path(r'^index/$', views.index,name='index_page'), # 路径index/的别名为index_page
]
```
##### views.py
```
from django.shortcuts import render 
from django.shortcuts import reverse # 用于反向解析
from django.shortcuts import redirect #用于重定向页面
from django.shortcuts import HttpResponse

def login(request):
    if request.method == 'GET':
        # 当为get请求时，返回login.html页面,页面中的{% url 'login_page' %}会被反向解析成路径：/login/
        return render(request, 'login.html')

    # 当为post请求时，可以从request.POST中取出请求体的数据
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    if name == 'kevin' and pwd == '123':
        url = reverse('index_page')  # reverse会将别名'index_page'反向解析成路径：/index/       
        return redirect(url) # 重定向到/index/
    else:
        return HttpResponse('用户名或密码错误')


def index(request):
    return render(request, 'index.html')
```
##### login.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录页面</title>
</head>
<body>
<!--强调：login_page必须加引号-->
<form action="{% url 'login_page' %}" method="post">
    {% csrf_token %} <!--强调：必须加上这一行，后续我们会详细介绍-->
    <p>用户名：<input type="text" name="name"></p>
    <p>密码：<input type="password" name="pwd"></p>
    <p><input type="submit" value="提交"></p>

</form>
</body>
</html>
```
##### index.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
<h3>我是index页面...</h3>
</body>
</html>
```
##### 说明
```
如果后期index的路径修改成这样：re_path(r'^i/$', views.index,name='index_page')
登录后依然可以正确跳转到相应的页面http://127.0.0.1:8000/i/
```
##### 总结
```
在views.py中，反向解析的使用：
    url = reverse('index_page')
在模版login.html文件中，反向解析的使用
    {% url 'login_page' %}
```
#### 存在分组的反向解析
```
from django.contrib import admin
from django.urls import path,re_path
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^article/(\d+)/$',views.article,name='article_page'), #　普通分组
    re_path(r'^user/(?P<uid>\d+)/$',views.article,name='user_page'), # 命名分组
]
# 1 针对普通分组，比如我们要反向解析出：/article/1/ 这种路径，写法如下
在views.py中，反向解析的使用：
    url = reverse('article_page',args=(1,)) 
在模版login.html文件中，反向解析的使用
    {% url 'article_page' 1 %}


# 2 针对命名分组，比如我们要反向解析出：/user/1/ 这种路径，写法如下
在views.py中，反向解析的使用：
    url = reverse('user_page',kwargs={'uid':1}) 
在模版login.html文件中，反向解析的使用
    {% url 'user_page' uid=1 %}

# ps:如果有多个参数，按空格分隔开即可
{% url 'xxx_page' 1 2 %}
{% url 'yyy_page' a=1 b=2 %}
```
# django2.x中的path
path是django2中新增的功能，用来解决数据类型转换问题和正则表达式冗余问题，出现了一个数据类型转换器的概念
### 示例
##### urls.py
```
from django.urls import re_path

from app01 import views

urlpatterns = [
    # 问题一：数据类型转换
    # 正则表达式会将请求路径中的年份匹配成功然后以str类型传递函数year_archive，在函数year_archive中如果想以int类型的格式处理年份，则必须进行数据类型转换
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),

    # 问题二：正则表达式冗余
    # 下述三个路由中匹配article_id采用了同样的正则表达式，重复编写了三遍，存在冗余问题，并且极不容易管理，因为一旦article_id规则需要改变，则必须同时修改三处代码

    re_path(r'^article/(?P<article_id>[a-zA-Z0-9]+)/detail/$', views.detail_view),
    re_path(r'^articles/(?P<article_id>[a-zA-Z0-9]+)/edit/$', views.edit_view),
    re_path(r'^articles/(?P<article_id>[a-zA-Z0-9]+)/delete/$', views.delete_view),
]
```
##### 使用path后如下：
```
from django.urls import path,re_path

from app01 import views

urlpatterns = [
    # 问题一的解决方案：
    path('articles/<int:year>/', views.year_archive), # <int:year>相当于一个有名分组，其中int是django提供的转换器，相当于正则表达式，专门用于匹配数字类型，而year则是我们为有名分组命的名，并且int会将匹配成功的结果转换成整型后按照格式（year=整型值）传给函数year_archive


    # 问题二解决方法：用一个int转换器可以替代多处正则表达式
    path('articles/<int:article_id>/detail/', views.detail_view), 
    path('articles/<int:article_id>/edit/', views.edit_view),
    path('articles/<int:article_id>/delete/', views.delete_view),
]
```
### django支持的转换器
```
str,匹配除了路径分隔符（/）之外的非空字符串，这是默认的形式
int,匹配正整数，包含0。
slug,匹配字母、数字以及横杠、下划线组成的字符串。
uuid,匹配格式化的uuid，如 075194d3-6885-417e-a8a8-6c931e272f00。
path,匹配任何非空字符串，包含了路径分隔符（/）（不能用？）

path('articles/<int:year>/<int:month>/<slug:other>/', views.article_detail) 
# 针对路径http://127.0.0.1:8000/articles/2009/123/hello/，path会匹配出参数year=2009,month=123,other='hello'传递给函数article_detail
匹配月份的时候只是按照int的要求去匹配了整数，并不会按照月份只匹配两位数，针对这种需要自定义转换器
```