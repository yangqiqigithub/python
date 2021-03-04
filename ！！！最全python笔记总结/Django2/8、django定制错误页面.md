# web常见错误 
```
1、400：400 Bad Request 是由于明显的客户端错误（例如，格式错误的请求语法，太大的大小，无效的请求消息或欺骗性路由请求），服务器不能或不会处理该请求。
2、403：用户没有访问某一资源的权限
3、404：请求的url地址不存在
4、500：服务端出错
```
# 配置方式
##### 在templates目录下的顶层创建错误页面  
400.html、403.html、404.html、500.html  
件内容自定义，但文件名与放置位置不可改变  

templates/400.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>自定义400页面</h1>
</body>
</html>
```
templates/403.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>自定义403页面</h1>
<p>
    {{ exception }}
</p>
</body>
```
templates/404.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>自定义404页面</h1>
<p>
    {{ exception }}
</p>
</body>
</html>
```
templates/500.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>自定义500页面</h1>
</body>
</html>
```
##### settings.py 中的 DEBUG设置为Fasle
```
DEBUG = False # 在生产环境中就应该设置成False

# ps：设置完DEBUG=False后，必须设置ALLOWED_HOSTS才能启动django，设为ALLOWED_HOSTS = ['*']即可
ALLOWED_HOSTS = ['*']
```
##### urls.py
```
from django.urls import path
from app01 import views

urlpatterns = [
    path('test/400',views.error_test_400),
    path('test/403',views.error_test_403),
    path('test/404',views.error_test_404),
    path('test/500',views.error_test_500),

]
```
##### views.py
```
from django.core.exceptions import SuspiciousFileOperation
from django.core.exceptions import PermissionDenied
from django.http import Http404


# 我们在编写正常视图view时会依据具体的逻辑，主动或被动抛出相对应的异常类型，此处为了测试精简，省略了正常逻辑，直接抛出异常
def error_test_400(request):
    raise SuspiciousFileOperation('抛出400异常') # 异常信息不会展现在页面中


def error_test_403(request):
    raise PermissionDenied('抛出403异常') # 异常信息会展现在页面中


def error_test_404(request):
    raise PermissionDenied('抛出404异常') # 异常信息会展现在页面中

def error_test_500(request):
    xxx # 会抛出异常NameError，异常信息不会展现在页面中
```
##### 测试
```
# 在浏览器依次输入下述url地址，会执行对应的视图函数，触发异常，django内置的异常处理视图会捕捉异常并返回我们定制的错误页面
http://127.0.0.1:8002/test/400
http://127.0.0.1:8002/test/403
http://127.0.0.1:8002/test/404
http://127.0.0.1:8002/test/500
```