# json序列化
如果我们要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式，比如XML，但更好的方法是序列化为JSON，因为JSON表示出来就是一个字符串，可以被所有语言读取，也可以方便地存储到磁盘或者通过网络传输。JSON不仅是标准格式，并且比XML更快，而且可以直接在Web页面中读取，非常方便。

但是也不是万能的，只能针对一些简单的数据类型，毕竟java和python还是有差距的
![image](4F66A9A1DD1442068199A52DCC1135B0)

##### Json.dump() json.load() 可以直接写入和读出
```
import json

dic={
    "name":"alex",
    "age":24,
    "hobby":"pingpang"
}
#
#json.dump()
with open("aa.txt",'w',encoding="utf8") as f:
    json.dump(dic,f)

#json.load()
with open("aa.txt",'r',encoding="utf8") as f2:
    print(json.load(f2))
```
##### json.dumps()  json.loads()
```
#json.dumps()
with open("bb.txt","w",encoding="utf8") as f3:
    f3.write(json.dumps(dic))

#json.loads()
with open("bb.txt","r",encoding="utf8") as f4:
    data=f4.read()
    dic=json.loads(data)
    print(dic)
```
# pickle序列化
Pickle的问题和所有其他编程语言特有的序列化问题一样，就是它只能用于Python，并且可能不同版本的Python彼此都不兼容，因此，只能用Pickle保存那些不重要的数据，不能成功地反序列化也没关系
##### pickle.dump()  pickle.load() 
```
import pickle
dic={
    "name":"alex",
    "age":24,
    "hobby":"pingpang"
}

#pickle.dump()
with open("pp.txt","wb") as f:
    pickle.dump(dic,f)
    '''
    pp.txt 里看起来像乱码一样 是pickle特有的规则
    '''
    
#pickle.load()
with open("pp.txt","rb") as f2:
    print(pickle.load(f2))
```
##### pickle.dumps()  pickle.loads()
```
#pickle.dumps()
with open("kk.txt","wb") as f:
    f.write(pickle.dumps(dic))

#pickle.loads()
with open("kk.txt","rb") as f:
    data=f.read()
    print(pickle.loads(data))
```