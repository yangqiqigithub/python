# FBV和CBV
```
1、FBV基于函数的视图（Function base views）

2、CBV基于类的视图(Class base views)
```
# FBV和CBV对比
### CBV
urls.py
```
from django.urls import path
from myapp import views
urlpatterns = [
    path('about/', views.MyView.as_view()),
]
#xx.类名.as_view()
```
views.py
```
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request):
        return HttpResponse('GET result')

    def post(self, request):
        return HttpResponse('POST result')
```
### FBV
urls.py
```
from django.urls import path
from myapp import views
urlpatterns = [
    path('about/', views.MyView),
]
```
views.py
```
from django.http import HttpResponse

def my_view(request):
    if request.method == 'GET':
        return HttpResponse('GET result')
    elif request.method == 'POST':
        return HttpResponse('POST result')
```
# CBV添加装饰器
CBV，当请求过来后会先执行dispatch()这个方法进而分发到对用的get、post方法上，所以如果需要批量装饰处理请求的方法（如get，post等）可以为dispatch方法添加装饰
```
# views.py
from django.shortcuts import render, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import time

# 装饰器
def timer(func):
    def wrapper(request, *args, **kwargs):
        start = time.time()
        ret = func(request, *args, **kwargs)
        print("函数执行的时间是{}".format(time.time() - start))
        return ret

    return wrapper

# CBV视图
class LoginView(View):
    #相当于给get,post请求都加上了装饰器
    @method_decorator(timer)
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'egon' and password == '123':
            return HttpResponse('登录成功')
        else:
            return HttpResponse('账号或密码错误')
```
单独装饰不同的方法，如
```
class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    @method_decorator(timer) # 只装饰get方法
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'egon' and password == '123':
            return HttpResponse('登录成功')
        else:
            return HttpResponse('账号或密码错误')
```
更简洁一点，我们可以把装饰器加在类上，通过name参数指定要装饰的方法，如下
```
# @method_decorator(timer,name='dispatch') # 批量添加
@method_decorator(timer,name='get') # 单独给get方法添加
# @method_decorator(timer,name='post') # 单独给post方法添加
class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'egon' and password == '123':
            return HttpResponse('登录成功')
        else:
            return HttpResponse('账号或密码错误')
```
如果有多个装饰器需要添加，可以定义一个列表或者元组将其存放起来，然后按照下述方式指定
```
from django.shortcuts import render, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import time

# 定义多个装饰
def deco1(func):
    def wrapper(request, *args, **kwargs):
        print('===>deco1')
        ret = func(request, *args, **kwargs)
        return ret
    return wrapper

def deco2(func):
    def wrapper(request, *args, **kwargs):
        print('===>deco2')
        ret = func(request, *args, **kwargs)
        return ret
    return wrapper

# 定义装饰列表
decorators = [deco1, deco2]

@method_decorator(decorators,name='get') # 为get方法添加多个装饰器
class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'egon' and password == '123':
            return HttpResponse('登录成功')
        else:
            return HttpResponse('账号或密码错误')
上述装饰器会按照列表规定的顺序依次执行装饰器
```