在python2中是大写 ConfigParser  
在python3中是小写 configparser  
用于生成和修改常见配置文档，利用字典进行处理  

例如如下文档：
![image](11956134E7E64216A375B545D1E0FDBC)

##### 如何生成my.ini这样的文档代码如下
```
'''
写入文件 这两步是必须有的 死的
import configparser
config=configparser.ConfigParser()
'''
import configparser

config=configparser.ConfigParser()


config["DEFAULT"]={
                    'ServerAliveInterval': '45',
                    'Compression': 'yes',
                    'CompressionLevel': '9'
}

config['bitbucket.org'] = {}

config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Host Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'

with open("my.ini","w",encoding="utf8") as f:
    config.write(f) #注意这里 是这样写入 和常规思维相反
```
##### 读取文档内容
```
# '''
# 读取文件这四步是必须有的  死的
# import configparser
# config=configparser.ConfigParser()
# config.sections()
# config.read("my.ini")
#
# '''
import configparser
config=configparser.ConfigParser()
config.sections()
config.read("my.ini")

print(config["DEFAULT"]["compressionlevel"])
print(config["bitbucket.org"]["user"])
```
##### 修改文档内容
```
#直接在文件里删除一整个session  一段就没有了
sec=config.remove_section("topsecret.server.com")
config.write(open("my.ini","w"))
print(config.sections())

#判断 添加session
sec=config.has_section("topsecret.server.com")
print(sec) #True
SEC=config.add_section("qiqi.www.com")
config.write(open("my.ini","a+"))
# '''
# 文件里多了 [qiqi.www.com]
# '''

#添加 存在 不会覆盖
config.set("qiqi.www.com","age","21")
config.write(open("my.ini","a+"))
# '''
# [qiqi.www.com]
# age = 21
# '''

#删除option 删除age这条option
config.remove_option("qiqi.www.com","age")
config.write(open("my.ini","w"))
```