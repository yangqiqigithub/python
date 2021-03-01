# 迭代的概念
是一个重复的过程，每一次的重复都会基于上一次的结果而来     

比如研发开发代码的过程，每一个新的版本都是基于旧的更新 

目前用到迭代概念的：
```
l=["a","b","c","d","e"]
count=0
while  count < len(l):
    print(l[count])
    count+=1
'''
用到了迭代的概念
依次按照索引取出了列表的值
'''
```
像列表，元组，字符串这些都可以按照索引取值，是有序对象，那么对于字典，集合这些

没有索引的无序列对象又该如何一一取值呢
比如如下这个字典
```
dic={
    "k1":"v1",
    "k2":"v2",
    "k3":"v3"
}
```
这就用到了迭代器 以下进入正题

# 迭代器
#### 可迭代对象
可迭代对象（iterable）：凡是对象下有__iter__方法的都是可迭代对象
```
l=["a","b","c","d","e"] #列表
t=("a","b","c",) #元组
dic={"k1":"v1","k2":"v2","k3":"v3"} #字典
s={"a","b","c","d","e"} #集合
f=open("users","w") #文件

l.__iter__()
t.__iter__()
print(dic.__iter__())
'''
<dict_keyiterator object at 0x000000E9269E2D68>
'''
print(s.__iter__())
'''
<set_iterator object at 0x000000A2DA53A480>
'''
f.__iter__()

'''
以上这些都是可迭代对象，凡是有__iter__方法的都是可迭代对象，不仅仅是以上
这些
'''
```
#### 迭代器
迭代器=可迭代对象.__iter__()   
可迭代对象.__iter__()的执行结果就是迭代器
```
l=["a","b","c","d","e"] #列表
print(l.__iter__())
'''
<list_iterator object at 0x00D8C470>
'''
```
当可迭代对象变成迭代器以后，就可以开心的一一取值了，通过next
```
dic={"k1":"v1","k2":"v2","k3":"v3"}
i=dic.__iter__()
while True:
    print(next(i))    
'''
循环取值
StopIteration 当没有值的时候出现 程序停止
'''
#捕获异常  避免程序中止
while True:
    try:
        print(next(i))
    except StopIteration: #增加异常处理 捕获异常
        break
```
#### 迭代器的优缺点
迭代器对象：
```
有__iter__()方法和__next__()方法；迭代器的__iter__()方法得到的依然是迭代器本身
#可迭代对象的__iter__()方法得到的是一个迭代器
```
迭代器对象的优点：
```
提供了一种统一的（不依赖索引的）的迭代方式
迭代器本身比起其他数据类型更省内存（每次只取一个值）
```
迭代器对象的缺点：
```
一次性取值，只能往后取值，不能回退，不如索引取值灵活
无法预知什么时候取值结束，即无法预知长度
```
# for循环的原理
```
l=["a","b","c","d"]

for i in l:
    print(i)

'''
for 会把要循环的对象l 执行 l.__iter__()方法得到一个迭代器对象
然后使用迭代器的__next__()方法，将每一次的值赋值给i，并且使用
try:
except 捕获异常
根据for循环的原理，可知只要是可迭代对象有__iter__()方法就可以
使用for循环
'''
```
# 文件本身就是一个迭代器
```
with open('test.py','r',encoding='utf8') as f:
    f.__next__()
    for line in f:
        print(f)
```
# 判断可迭代对象和迭代器的方法
迭代器一定是可迭代对象   
可迭代对象不一定是迭代器  
```
from collections import Iterable,Iterator
l=[1,2,3,4,5,6]
print(isinstance(l,Iterator))
print(isinstance(l,Iterable))
'''
False 
True
'''
```
常用的数据类型中 只有文件是迭代器对象