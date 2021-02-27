# 视图函数
在视图层，默认是views.py里的函数，用来处理请求和响应。  
研究视图函数，需要熟练掌握两个对象：         
**请求对象 HttpRequest**  
**响应对象 HttpResponse**   
# 请求对象 HttpRequest


```
if request.method == 'GET':
    # 当请求url为：http://127.0.0.1:8001/login/?a=1&b=2&c=3&c=4&c=5
    # 请求方法是GET，?后的请求参数都存放于request.GET中
    print(request.GET)
    # 输出<QueryDict: {'a': ['1'], 'b': ['2'], 'c': ['3', '4', '5']}>

    # 获取？后参数的方式为
    b=request.GET.get('b') # 2
    c=request.GET.getlist('c') # ['3', '4', '5']
    c1=request.GET.get('c') # 5
    
    # 针对请求的url地址：http://127.0.0.1:8001/order/?name=egon&age=10#_label3
    # 从域名后的最后一个“/”开始到“？”为止是路径部分，即/order/
    # 从“？”开始到“#”为止之间的部分为参数部分,即name=egon&age=10
    def order(request):
        print(request.path) # 结果为“/order/”
        print(request.get_full_path()) # 结果为"/order/?name=egon&age=10"


if request.method == 'POST':
    # 在输入框内输入用户名egon、年龄18，选择爱好，点击提交
    # 请求方法为POST，表单内的数据都会存放于request.POST中
    print(request.POST) 
    # 输出<QueryDict: {..., 'name': ['egon'], 'age': ['18'], 'hobbies': ['music', 'read']}>

    # 获取表单中数据的方式为
    name=request.POST.get('name') # egon
    age=request.POST.get('age') # 18
    hobbies=request.POST.getlist('hobbies') # ['music', 'read']
      
    # 接收文件的方式 
    obj = request.FILES.get('filename')  # 上传文件的时候就用 request.FILES 先获取文件对象
    filepath=os.path.join('upload',obj.name) #obj.name 文件名字
    f=open(filepath,mode='wb')
    for i in obj.chunks():#obj.chunks 将文件内容一点一点迭代传输
        f.write(i)
    f.close()
```
# 响应对象 HttpResponse
```
from django.shortcuts import HttpResponse 返回字符串
from django.shortcuts import redirect  重定向
from django.shortcuts import render 返回页面

from django.http import JsonResponse 返回json格式字符串
```
### HttpResponse
返回字符串
```
from django.http import HttpResponse
response = HttpResponse("Here's the text of the Web page.")
response = HttpResponse("Text only, please.", content_type="text/plain")

'''
ps：Content-Type用于指定响应体的MIME类型

MIME类型：
mime类型是多用途互联网邮件扩展类型。是设定某种扩展名的文件用一种应用程序来打开的方式类型,当该扩展名文件被访问的时候,浏览器会自动使用指定应用程序来打开


MIME 类型有非常多种，一般常见的有：

　　text/html：浏览器在获取到这种文件时会自动调用html的解析器对文件进行相应的处理。

　　text/plain：意思是将文件设置为纯文本的形式，浏览器在获取到这种文件时并不会对其进行处理。

　　image/jpeg：JPEG格式的图片

　　image/gif：GIF格式的图片

　　video/quicktime：Apple 的 QuickTime 电影

　　application/vnd.ms-powerpoint：微软的powerpoint文件
'''
```
###  render 
返回页面 
```
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'name': 'egon', 'tag': 'dsb'})
```
### redirect  
重定向302
```
from django.shortcuts import HttpResponse,redirect

def index(request):
    return redirect('/login/') # 跳转到http://127.0.0.1:8000/login/
    # return redirect('login/') # 跳转到http://127.0.0.1:8000/index/login/

def login(request):
    return HttpResponse("login page")
```
##### 重定向转态码301与302的区别
```
一、301和302的异同。
   1、相同之处：
   301和302状态码都表示重定向，具体点说就是浏览器在拿到服务器返回的这个状态码后会自动跳转到一个新的URL地址（浏览器会从响应头Location中获取新地址），用户看到的效果都是输入地址A后瞬间跳转到了另一个地址B

   2、不同之处：
　　301表示永久重定向，旧地址A的资源已经被永久地移除了，即这个资源不可访问了。
　　302表示临时重定向，旧地址A的资源还在，即这个资源仍然可以访问。

    A页面临时重定向到B页面，那搜索引擎收录的就是A页面。
    A页面永久重定向到B页面，那搜索引擎收录的就是B页面。
    从SEO层面考虑，302要好于301

二、重定向原因：
   1、网站调整（如改变网页目录结构）；
   2、网页被移到一个新地址；
   3、网页扩展名改变(如应用需要把.php改成.Html或.shtml)。
      这种情况下，如果不做重定向，则用户收藏夹或搜索引擎数据库中旧地址只能让访问客户得到一个404页面错误信息，访问流量白白丧失；再者某些注册了多个域名的网站，也需要通过重定向让访问这些域名的用户自动跳转到主站点等。
```
### JsonResponse 
返回json格式字符串
向前端返回一个json格式字符串的两种方式  
方式一：
```
import json

def my_view(request):
    data=['egon','kevin']
    return HttpResponse(json.dumps(data) )
```
方式二：
```
from django.http import JsonResponse

def my_view(request):
    data=['egon','kevin']
    return JsonResponse(data,safe=False)
    #默认safe=True代表只能序列化字典对象，safe=False代表可以序列化字典以外的对象
```