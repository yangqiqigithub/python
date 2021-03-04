# 示例
views.py
```
from django.shortcuts import render
import time

# 返回静态内容(静态页面)
def index(request):
    return render(request,'index.html')

# 返回动态内容(动态页面)
def current_datetime(request):
    now_time = time.strftime('%Y-%m-%d %X')
    context={"now":now_time}
    return render(request,'current_datetime.html',context)
```
urls.py
```
from django.urls import path
from app01.views import *

urlpatterns = [
    path('index/', index),
    path('current_datetime/', current_datetime),
]
```
# 模板引擎配置
settings.py
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
# 模板语法
### 变量的基本使用
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<p>{{ name }}</p>
<p>{{ sex }}</p>

</body>
</html>
```
### 句点符深度查询
点后的可以是字典相关（字典的key或者字典内置方法）、对象的属性或方法、数字索引
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<!--调用字符串对象的upper方法，注意不要加括号-->
<p>{{ msg.upper }}</p>

<!--取字典中k1对应的值-->
<p>{{ dic.k1 }}</p>

<!--取对象的name属性-->
<p>{{ obj.name }}</p>

<!--取列表的第2个元素,然后变成大写-->
<p>{{ li.1.upper }}</p>

<!--取列表的第3个元素，并取该元素的age属性-->
<p>{{ li.2.age }}</p>

</body>
</html>
```
### 过滤器
```
#default
#作用：如果一个变量值是False或者为空、None，使用default后指定的默认值，否则，使用变量本身的值，如果value=’‘则输出“nothing”
{{ value|default:"nothing" }}

#default_if_none
#作用：如果只针对value是None这一种情况来设置默认值，需要使用default_if_none
#只有在value=None的情况下，才会输出“None...”，
{{ value|default_if_none:"None..." }}

#length
#作用：返回值的长度。它对字符串、列表、字典等容器类型都起作用，如果value是 ['a', 'b', 'c', 'd']，那么输出是4
{{ value|length }}

#filesizeformat
#作用：将值的格式化为一个"人类可读的"文件尺寸(如13KB、4.1 MB、102bytes等等），如果 value 是 12312312321，输出将会是 11.5 GB
{{ value|filesizeformat }}

#date
#作用：将日期按照指定的格式输出，如果value=datetime.datetime.now(),按照格式Y-m-d则输出2019-02-02
{{ value|date:"Y-m-d" }}　　

#slice
#作用：对输出的字符串进行切片操作，顾头不顾尾,如果value=“egon“，则输出"eg"
{{ value|slice:"0:2" }}　

#truncatechars
#作用：如果字符串字符多于指定的字符数量，那么会被截断。截断的字符串将以可翻译的省略号序列（“...”）结尾，如果value=”hello world egon 嘎嘎“，则输出"hello...",注意8个字符也包含末尾的3个点
{{ value|truncatechars:8 }}

#truncatewords
#作用：同truncatechars，但truncatewords是按照单词截断，注意末尾的3个点不算作单词，如果value=”hello world egon 嘎嘎“，则输出"hello world ..."
{{ value|truncatewords:2 }}

```
### HTML的自动转义
一个用户注册时故意输入自己的用户名为：
```
<script>alert('hello')</script>
```
后台取出name = "alert('hello')"，然后执行render渲染的结果为
```
Hello, <script>alert('hello')</script>
```
上述结果交给浏览器后，意味着浏览器将弹出一个JavaScript警报框！试想，如果是一个博客类网站，恶意作者在自己提交的文章中掺杂了类似上面这种恶意代码，这意味着每个读者在读取他的文章时，自己的浏览器都会弹出一个JavaScript警报框！

以上情况django已经为了做了相应的处理：django的模板引擎在生成模板时，默认就会对所有变量的值进行转义，具体是针对变量值中包含的以下五个字符的转义
```
# 1、使用DTL，以下5种特殊符号默认就会被转义成对应的html命名实体
1、< 被转换成 &lt;
2、> 被转换成 &gt;
3、' 单引号被转换成 &#x27;
4、" 双引号被转换成 &quot;
5、& 被转换成 &amp;

# 首先经过转义后得到模板，然后递交给浏览器解析，上述内容均会被当成普通字符输出
例如：
针对value="<script>alert(123)</script>"，模板变量{{ value }}会被渲染成&lt;script&gt;alert(123)&lt;/script&gt;交给浏览器后会被解析成普通字符”<script>alert(123)</script>“，失去了js代码的语法意义
```
但是有时候就希望django不要转义，直接显示代码，方法如下：
##### 针对单个变量->使用过滤器safe
```
比如如value='<a href="https://www.baidu.com">点我啊</a>'，经过过滤器safe的处理，浏览器在进行解析时就会将其当做超链接显示，不加safe过滤器则会当做普通字符显示’<a href="https://www.baidu.com">点我啊</a>‘
```
##### 针对模板块->使用标签autoescape
```
{# 对包含在标签内的模板块的转义行为进行整体关闭 #}
{% autoescape off %}
    <p>
        不会转义 {{ name }}.
    </p>

    {#  支持嵌套，设置嵌套的模板块整体开启转义功能 #}
    {% autoescape on %}
        <p>
            会被转义: {{ name }}
        </p>
    {% endautoescape %}
{% endautoescape %}
```
autoescape的效果会遗传给子模板（使用标签extends继承当前模板），也会留给引入了当前模板的模板
### 常用标签
##### for循环标签
```
#1、遍历每一个元素：
{% for person in person_list %}
    <p>{{ person.name }}</p>
{% endfor %}

#2、可以利用{% for obj in list reversed %}反向循环。

#3、遍历一个字典：
{% for key,val in dic.items %}
    <p>{{ key }}:{{ val }}</p>
{% endfor %}

#4、循环序号可以通过{{ forloop }}显示　
forloop.counter            当前循环的索引值（从1开始）
forloop.counter0           当前循环的索引值（从0开始）
forloop.revcounter         当前循环的倒序索引值（从1开始）
forloop.revcounter0        当前循环的倒序索引值（从0开始）
forloop.first              当前循环是第一次循环则返回True，否则返回False
forloop.last               当前循环是最后一次循环则返回True，否则返回False
forloop.parentloop         本层循环的外层循环

#5、for标签可以带有一个可选的{% empty %} 从句，在变量person_list为空或者没有被找到时，则执行empty子句
{% for person in person_list %}
    <p>{{ person.name }}</p>

{% empty %}
    <p>sorry,no person here</p>
{% endfor %}
```
##### if 条件语句标签
```
# 1、注意：
{% if 条件 %}条件为真时if的子句才会生效，条件也可以是一个变量，if会对变量进行求值，在变量值为空、或者视图没有为其传值的情况下均为False

# 2、具体语法
{% if num > 100 or num < 0 %}
    <p>无效</p>
{% elif num > 80 and num < 100 %}
    <p>优秀</p>
{% else %}
    <p>凑活吧</p>
{% endif %}

#3、if语句支持 and 、or、==、>、<、!=、<=、>=、in、not in、is、is not判断。

#4、判断条件中可以引入过滤器
{% if athlete_list|length > 1 %}
   Team: {% for athlete in athlete_list %} ... {% endfor %}
{% else %}
   Athlete: {{ athlete_list.0.name }}
{% endif %}

过滤器length返回的数字可用于与数字进行比较，除此之外大多数过滤器返回的都是字符串并不能用于与数字比较

#5、补充标签firstof
针对下述多分支
    {% if var1 %}
        {{ var1 }}
    {% elif var2 %}
        {{ var2 }}
    {% elif var3 %}
        {{ var3 }}
    {% endif %}

可以简写为一行
    {% firstof var1 var2 var3 %}

也可以定义一个备用值，当var1、var2、var3均无值的时使用
{% firstof var1 var2 var3 "fallback value" %}

还可以使用as语法，将firsof得到的值赋值给一个变量value，以后在模板中使用{{ value }}即可
{% firstof var1 var2 var3 "fallback value" as value %}
```
##### with标签
```
# with标签用来为一个复杂的变量名起别名,如果变量的值来自于数据库，在起别名后只需要使用别名即可，无需每次都向数据库发送请求来重新获取变量的值
{% with li.1.upper as v %}
    {{ v }}
{% endwith %}
``
##### csrf_token
```
#####  csrf_token标签
```
# 当用form表单提交POST请求时必须加上标签{% csrf_token%}，该标签用于防止跨站伪造请求
<form action="" method="POST">
    {% csrf_token %}
    <p>用户名：<input type="text" name="name"></p>
    <p>密码：<input type="password" name="pwd"></p>
    <p><input type="submit" value="提交"></p>
</form>
# 具体工作原理为：
# 1、在GET请求到form表单时，标签{% csrf_token%}会被渲染成一个隐藏的input标签，该标签包含了由服务端生成的一串随机字符串,如<input type="hidden" name="csrfmiddlewaretoken" value="dmje28mFo...OvnZ5">
# 2、在使用form表单提交POST请求时，会提交上述随机字符串，服务端在接收到该POST请求时会对比该随机字符串，对比成功则处理该POST请求，否则拒绝，以此来确定客户端的身份
```
# 模板的导入和继承
### 模板的导入 include
在一个模板文件中，引入/重用另外一个模板文件的内容
```
{% include '模版名称' %}
```
示例：  
teachers.html --- 专门介绍每个老师的资质
index.html  
需要在index.html里引用teacher.html里的内容
```
# index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
        }

        .header {
            height: 50px;
            width: 100%;
            background-color: black;
        }

    </style>
</head>
<body>
<div class="header"></div>
<div class="container">
    <div class="row">
        <div class="col-md-3">
            <!--在index.html引入teachers.html文件的内容-->
            {% include "teachers.html" %}
        </div>
        <div class="col-md-9"></div>
    </div>
</div>
</body>
</html>
```
### 模板的继承
base.html 定义了网站页面的大结构  
index.html需要继承base.html里的结构
##### base.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>
        {% block title %}自定义title名{% endblock %}
    </title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css">

</head>
<body>
<div class="header"></div>

<div class="container">
    <div class="row">
        <div class="col-md-3">
            <div class="list-group">
                {% block sidebar %}
                   
                {% endblock %}

            </div>
        </div>

        <div class="col-md-9">
            {% block content %}

            {% endblock %}
        </div>
    </div>

</div>

</body>
</html>
```
##### index.html
```
{% extends "base.html" %}

<!--用新内容完全覆盖了父模板内容-->
{% block title %}
    index页面
{% endblock %}


{% block sidebar %}
    <!--该变量会将父模板中sidebar中原来的内容继承过来，然后我们可以在此基础上新增，否则就是纯粹地覆盖-->
    {{ block.super }}

    <!--在继承父模板内容的基础上新增的标签-->
    <a href="#" class="list-group-item">拍卖</a>
    <a href="#" class="list-group-item">金融</a>
{% endblock %}

{% block content %}
    <!--用新内容完全覆盖了父模板内容-->
    <p>index页面内容</p>
{% endblock %}
```
# 静态文件的配置
### 单app下静态文件的配置
settings.py
```
STATIC_URL = '/static/' # 找到这一行，然后新增下述代码
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'statics'),# 获取静态文件在服务端的绝对路径
]
```
模板index.html里的引用
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="/static/css/my.css">
</head>
<body>
<img src="/static/img/rb.jpeg" alt="">

<script src="/static/js/jquery-3.3.1.min.js"></script>
<script src="/static/js/my.js"></script>

</body>
```
### 多app下静态文件的组织和使用
##### 假如目录结构
```
├── app01
│   ├── static
│   │   └── a.css # 文件内容为：h1 { color: red; }
├── app02
│   ├── static
│   │   └── a.css # 文件内容为：h1 { color: green; }
├── static
│   └── a.css     # 文件内容为：h1 { color: blue; }
├── static1
│   └── a.css     # 文件内容为：h1 { color: goldenrod; }
├── templates
│   └── index.html
```
##### settings.py
```
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "static1"),
]
```
##### 模板index.html里的引用
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    {% load static %}

    <link rel="stylesheet" href="{% static "a.css" %}">
</head>
<body>
<h1>模板内容</h1>
</body>
</html>
```
静态文件的加载优先级模板的查找优先级是一样的原理，{% static "a.css" %}查找优先级为  
1、djanog首先会先依次检索STATICFILES_DIRS列表中的目录  
2、然后按照配置项INSTALLED_APPS注册的app顺序，依次检索每个app下的static目录  

为了避免出现冲突，与模板的组织原理一样，我们可以在每个static下创建子目录来充当名称空间的作用，所以上述目录结构调整为   
```
├── app01
│   ├── static
│   │   └── app01
│   │       └── a.css
├── app02
│   ├── static
│   │   └── app02
│   │       └── a.css
├── static
│   └── base
│       └── a.css
├── static1
│   └── base1
│       └── a.css
├── templates
│   └── index.html
```
模板index.html中引入静态文件a.css的路径如下，即便静态文件重名，也不会发生冲突
```
<link rel="stylesheet" href="{% static "base/a.css" %}">

<link rel="stylesheet" href="{% static "base1/a.css" %}">

<link rel="stylesheet" href="{% static "app01/a.css" %}">

<link rel="stylesheet" href="{% static "app02/a.css" %}">
```