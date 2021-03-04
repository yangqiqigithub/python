# 客户端/服务端架构 

c/s架构  
腾讯作为服务端，下载个腾讯视频客户端才能查看腾讯视频

b/s架构（也是c/s架构的一种）  
访问网站，浏览器是客户端  

我们学习socket就是为了完成C/S的开发  

# osi七层
![image](6189F7E5EEB74C07A390AFD4EE0D9F9A)

# socket层
![image](EA2D3B0AAE6D4FEFAF261DC7DA6A9542)

# socket是什么
Socket是应用层与TCP/IP协议族通信的中间软件抽象层，它是一组接口。在设计模式中，Socket其实就是一个门面模式，它把复杂的TCP/IP协议族隐藏在Socket接口后面，对用户来说，一组简单的接口就是全部，让Socket去组织数据，以符合指定的协议。

# 套接字
套接字起源于 20 世纪 70 年代加利福尼亚大学伯克利分校版本的 Unix,即人们所说的 BSD Unix。 因此,有时人们也把套接字称为“伯克利套接字”或“BSD 套接字”。一开始,套接字被设计用在同 一台主机上多个应用程序之间的通讯。这也被称进程间通讯,或 IPC。套接字有两种（或者称为有两个种族）,分别是基于文件型的和基于网络型的。

**基于文件类型的套接字家族**

套接字家族的名字：AF_UNIX

unix一切皆文件，基于文件的套接字调用的就是底层的文件系统来取数据，两个套接字进程运行在同一机器，可以通过访问同一个文件系统间接完成通信

**基于网络类型的套接字家族**

套接字家族的名字：AF_INET

(还有AF_INET6被用于ipv6，还有一些其他的地址家族，不过，他们要么是只用于某个平台，要么就是已经被废弃，或者是很少被使用，或者是根本没有实现，所有地址家族中，AF_INET是使用最广泛的一个，python支持很多种地址家族，但是由于我们只关心网络编程，所以大部分时候我么只使用AF_INET)

# 套接字的工作流程
![image](519F3B6E8EC8471E89DDF00834014404)

### 示例
##### server端
```
#用打电话模拟 socket服务端通信的流程

import  socket


#买手机 初始化socket
phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #实例化一个socket对象

#插卡 绑定端口
phone.bind(('127.0.0.1',8080)) #绑定自己的ip+port，就像手机号，客户端就是通过这个来找服务端的

#开机 监听端口
phone.listen(5)  #开始监听 最大允许挂起的连接数为5

#等待电话打入 等待接收客户端发过来的连接请求  一旦有就接收  调用accept阻塞，等待客户端连接
print('server starts ...')
conn,client_addr=phone.accept() #得到的是一个元组（建立好的连接对象，客户端ip）使用变量解压


#基于建立的连接，收发消息，进行通话
client_data=conn.recv(1024) #接受客户端发过来的数据 一次最大收1024
print("客户端发过来的消息",client_data.decode())
conn.send(client_data.upper()) #发送消息给客户端 这里表示把数据都大写一下返回回去

#挂电话
conn.close()


#关机
phone.close()
```
##### client端
```
import socket

#买手机 初始化socket
phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


#给服务端打电话  连接服务端
phone.connect(('127.0.0.1',8080))
'''
客户端不需要ip和端口  服务器端的ip和端口是为了让客户端去找到自己
然后客户端通过ip+端口找到服务端，建立连接，通过这条间接通道通信
这里客服端去连接服务端后，没什么意外就建立连接了

'''

#和服务端互发消息 进行通信
phone.send('hello'.encode('utf8'))  #网络只认识二进制，转成bytes类型
server_data=phone.recv(1024) #接收服务端发来的消息
print('服务端回应的消息',server_data.decode())

#关机
phone.close()
```
### 常用方法

```
import  socket
# 初始化socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #tcp
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #udp

# 服务端套接字函数
s.bind()    绑定(主机,端口号)到套接字
s.listen()  开始TCP监听
s.accept()  被动接受TCP客户的连接,(阻塞式)等待连接的到来

# 客户端套接字函数
s.connect()     主动初始化TCP服务器连接
s.connect_ex()  connect()函数的扩展版本,出错时返回出错码,而不是抛出异常

# 公共用途的套接字函数
s.recv()            接收TCP数据
s.send()            发送TCP数据(send在待发送数据量大于己端缓存区剩余空间时,数据丢失,不会发完)
s.sendall()         发送完整的TCP数据(本质就是循环调用send,sendall在待发送数据量大于己端缓存区剩余空间时,数据不丢失,循环调用send直到发完)
s.recvfrom()        接收UDP数据
s.sendto()          发送UDP数据
s.getpeername()     连接到当前套接字的远端的地址
s.getsockname()     当前套接字的地址
s.getsockopt()      返回指定套接字的参数
s.setsockopt()      设置指定套接字的参数
s.close()           关闭套接字

# 面向锁的套接字方法
s.setblocking()     设置套接字的阻塞与非阻塞模式
s.settimeout()      设置阻塞套接字操作的超时时间
s.gettimeout()      得到阻塞套接字操作的超时时间

# 面向文件的套接字的函数
s.fileno()          套接字的文件描述符
s.makefile()        创建一个与该套接字相关的文件
```
# 基于TCP的套接字
### 简单示例
##### server端
加了上通信循环，连接循环，重用地址
```
import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #地址重用
s.bind(('127.0.0.1',8080))
s.listen(5)

while True: #连接循环
    conn, client_addr = s.accept()
    print('客户端的连接地址为：%s' % (conn))
    while True: #通信循环
       try:
           data = conn.recv(1024)
           if not data:break
           print('客户端发过来的消息为：%s' % (data.decode('gbk')))
           conn.send(data.upper())
       except Exception as e:
           break
    conn.close()

s.close()
```
![image](3DF8AB1102E745A297157310D0271D52)
解决方法：
```
import socket
##在bind前加上这条即可  重用地址
phone.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
```
##### client端
```
import socket

c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(('127.0.0.1',8080))

while True:
    msg=input('输入命令>>:').strip()
    if msg=='exit':
        break
    if not msg:continue
    c.send(msg.encode('utf8'))
    data=c.recv(1024)
    print('服务端返回消息为：%s' %data.decode('gbk'))
c.close()
```
### 模拟ssh执行命令
##### server端
```
import  socket
import subprocess

phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #实例化一个socket对象
phone.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #就是它，在bind前加

phone.bind(('127.0.0.1',8080)) #绑定自己的ip+port，

phone.listen(5)  #开始监听 最大允许挂起的连接数为5

print('server starts ...')
while True: #连接循环
    conn,client_addr=phone.accept()
    print(conn)

    #基于建立的连接，收发消息，进行通话
    while True: #通信息循环
        try:
            cmd_data=conn.recv(1024) #接受客户端发过来的数据 一次最大收1024
            if not cmd_data:break #针对Linux系统加上这条Linux和mac即使客户端死了
                                    # 服务端不会死 只是一直收取空消息
            #执行命令拿到结果
            res=subprocess.Popen(cmd_data.decode('utf8'),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell=True)
            res_err=res.stderr.read()
            res_out=res.stdout.read()
            conn.send(res_err+res_out)
        except Exception: #解决了 客户端单方面死了  服务端也死 但是不抛出异常  好看一些
            break

    #挂电话
    conn.close()
#关机
phone.close()
```
##### client端
```
import socket
import os

phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

phone.connect(('127.0.0.1',8080))

#和服务端互发消息 进行通信
while True: #通信循环
    cmd=input('>>:')
    if not cmd:continue
    #发送命令
    phone.send(cmd.encode('utf8'))  #网络只认识二进制，转成bytes类型
    #收取命令的执行结果
    cmd_res=phone.recv(1024)
    #打印结果
    print(cmd_res.decode('gbk'))

#关机
phone.close()
```
# 基于UDP的套接字
udp是无链接的，先启动哪一端都不会报错
### 简单示例
##### server端
```
import socket
ip_port=('127.0.0.1',9000)
BUFSIZE=1024
udp_server_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

udp_server_client.bind(ip_port)

while True:
    msg,addr=udp_server_client.recvfrom(BUFSIZE)
    print(msg,addr)

    udp_server_client.sendto(msg.upper(),addr)
```
##### client端
```
import socket
ip_port=('127.0.0.1',9000)
BUFSIZE=1024
udp_server_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    msg=input('>>: ').strip()
    if not msg:continue

    udp_server_client.sendto(msg.encode('utf-8'),ip_port)

    back_msg,addr=udp_server_client.recvfrom(BUFSIZE)
    print(back_msg.decode('utf-8'),addr)
```
### qq聊天
由于udp无连接，所以可以同时多个客户端去跟服务端通信
##### server端
```
import socket
ip_port=('127.0.0.1',8081)
udp_server_sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #买手机
udp_server_sock.bind(ip_port)

while True:
    qq_msg,addr=udp_server_sock.recvfrom(1024)
    print('来自[%s:%s]的一条消息:\033[1;44m%s\033[0m' %(addr[0],addr[1],qq_msg.decode('utf-8')))
    back_msg=input('回复消息: ').strip()

    udp_server_sock.sendto(back_msg.encode('utf-8'),addr)
```
##### client-1端
```
import socket
BUFSIZE=1024
udp_client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

qq_name_dic={
    '狗哥alex':('127.0.0.1',8081),
    '瞎驴':('127.0.0.1',8081),
    '一棵树':('127.0.0.1',8081),
    '武大郎':('127.0.0.1',8081),
}


while True:
    qq_name=input('请选择聊天对象: ').strip()
    while True:
        msg=input('请输入消息,回车发送: ').strip()
        if msg == 'quit':break
        if not msg or not qq_name or qq_name not in qq_name_dic:continue
        udp_client_socket.sendto(msg.encode('utf-8'),qq_name_dic[qq_name])

        back_msg,addr=udp_client_socket.recvfrom(BUFSIZE)
        print('来自[%s:%s]的一条消息:\033[1;44m%s\033[0m' %(addr[0],addr[1],back_msg.decode('utf-8')))

udp_client_socket.close()
```
##### client-2端
```
import socket
BUFSIZE=1024
udp_client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

qq_name_dic={
    '狗哥alex':('127.0.0.1',8081),
    '瞎驴':('127.0.0.1',8081),
    '一棵树':('127.0.0.1',8081),
    '武大郎':('127.0.0.1',8081),
}


while True:
    qq_name=input('请选择聊天对象: ').strip()
    while True:
        msg=input('请输入消息,回车发送: ').strip()
        if msg == 'quit':break
        if not msg or not qq_name or qq_name not in qq_name_dic:continue
        udp_client_socket.sendto(msg.encode('utf-8'),qq_name_dic[qq_name])

        back_msg,addr=udp_client_socket.recvfrom(BUFSIZE)
        print('来自[%s:%s]的一条消息:\033[1;44m%s\033[0m' %(addr[0],addr[1],back_msg.decode('utf-8')))

udp_client_socket.close()
```
### 时间服务器
##### server端
```
from socket import *
from time import strftime

ip_port=('127.0.0.1',9000)
bufsize=1024

tcp_server=socket(AF_INET,SOCK_DGRAM)
tcp_server.bind(ip_port)

while True:
    msg,addr=tcp_server.recvfrom(bufsize)
    print('===>',msg)

    if not msg:
        time_fmt='%Y-%m-%d %X'
    else:
        time_fmt=msg.decode('utf-8')
    back_msg=strftime(time_fmt)

    tcp_server.sendto(back_msg.encode('utf-8'),addr)

tcp_server.close()
```
##### client端
```
from socket import *
ip_port=('127.0.0.1',9000)
bufsize=1024

tcp_client=socket(AF_INET,SOCK_DGRAM)


while True:
    msg=input('请输入时间格式(例%Y %m %d)>>: ').strip()
    tcp_client.sendto(msg.encode('utf-8'),ip_port)
    data=tcp_client.recv(bufsize)
    print(data.decode('utf-8'))

tcp_client.close()
```
# 粘包
### 什么是粘包以及产生原因
只有TCP有粘包现象，UDP永远不会粘包

首先需要掌握一个socket收发消息的原理
![image](2E9E6A82FB3C4E1989CEF4D46874C011)


发送端可以是一K一K地发送数据，而接收端的应用程序可以两K两K地提走数据，当然也有可能一次提走3K或6K数据，或者一次只提走几个字节的数据，也就是说，应用程序所看到的数据是一个整体，或说是一个流（stream），一条消息有多少字节对应用程序是不可见的，因此TCP协议是面向流的协议，这也是容易出现粘包问题的原因。而UDP是面向消息的协议，每个UDP段都是一条消息，应用程序必须以消息为单位提取数据，不能一次提取任意字节的数据，这一点和TCP是很不同的。怎样定义消息呢？可以认为对方一次性write/send的数据为一个消息，需要明白的是当对方send一条信息的时候，无论底层怎样分段分片，TCP协议层会把构成整条消息的数据段排序完成后才呈现在内核缓冲区。

例如基于tcp的套接字客户端往服务端上传文件，发送时文件内容是按照一段一段的字节流发送的，在接收方看了，根本不知道该文件的字节流从何处开始，在何处结束

所谓粘包问题主要还是因为接收方不知道消息之间的界限，不知道一次性提取多少字节的数据所造成的。

此外，发送方引起的粘包是由TCP协议本身造成的，TCP为提高传输效率，发送方往往要收集到足够多的数据后才发送一个TCP段。若连续几次需要send的数据都很少，通常TCP会根据优化算法把这些数据合成一个TCP段后一次发送出去，这样接收方就收到了粘包数据。

TCP（transport control protocol，传输控制协议）是面向连接的，面向流的，提供高可靠性服务。收发两端（客户端和服务器端）都要有一一成对的socket，因此，发送端为了将多个发往接收端的包，更有效的发到对方，使用了优化方法（Nagle算法），将多次间隔较小且数据量小的数据，合并成一个大的数据块，然后进行封包。这样，接收端，就难于分辨出来了，必须提供科学的拆包机制。 即面向流的通信是无消息保护边界的。
UDP（user datagram protocol，用户数据报协议）是无连接的，面向消息的，提供高效率服务。不会使用块的合并优化算法，, 由于UDP支持的是一对多的模式，所以接收端的skbuff(套接字缓冲区）采用了链式结构来记录每一个到达的UDP包，在每个UDP包中就有了消息头（消息来源地址，端口等信息），这样，对于接收端来说，就容易进行区分处理了。 即面向消息的通信是有消息保护边界的。
tcp是基于数据流的，于是收发的消息不能为空，这就需要在客户端和服务端都添加空消息的处理机制，防止程序卡住，而udp是基于数据报的，即便是你输入的是空内容（直接回车），那也不是空消息，udp协议会帮你封装上消息头，实验略
udp的recvfrom是阻塞的，一个recvfrom(x)必须对唯一一个sendinto(y),收完了x个字节的数据就算完成,若是y>x数据就丢失，这意味着udp根本不会粘包，但是会丢数据，不可靠

tcp的协议数据不会丢，没有收完包，下次接收，会继续上次继续接收，己端总是在收到ack时才会清除缓冲区内容。数据是可靠的，但是会粘包。

两种情况下会发生粘包。

发送端需要等缓冲区满才发送出去，造成粘包（发送数据时间间隔很短，数据了很小，会合到一起，产生粘包）

接收方不及时接收缓冲区的包，造成多个包接收（客户端发送了一段数据，服务端只收了一小部分，服务端下次再收的时候还是从缓冲区拿上次遗留的数据，产生粘包）

无论是接收方还是发送方，接收或者发送的消息都是存放在自己的系统内存中，和对方无关

产生粘包的根本原因：
接收方不知道消息的开始和结束，不知道一次性提取多少才算提取完毕，而发送的机制根据算法，对于间隔时间短和消息量不大的时候，攒一攒，攒着一起发送，接收方每次最大接收1024字节

所以解决粘包问题的思路是：
发送方发送消息的时候，要想办法告诉接收方，消息的长度，接收方根据长度循环接收，直到全部接收完毕为止

# 解决粘包
### struct模块 
该模块可以把一个类型，如数字，转成固定长度的bytes
>>> struct.pack('i',1111111111111)
。。。。。。。。。
struct.error: 'i' format requires -2147483648 <= number <= 2147483647 #这个是范围
### 思路
```
import json,struct
#假设通过客户端上传1T:1073741824000的文件a.txt

#为避免粘包,必须自定制报头
header={'file_size':1073741824000,'file_name':'/a/b/c/d/e/a.txt','md5':'8f6fbf8347faa4924a76856701edb0f3'} #1T数据,文件路径和md5值

#为了该报头能传送,需要序列化并且转为bytes
head_bytes=bytes(json.dumps(header).encoding='utf-8') #序列化并转成bytes,用于传输

#为了让客户端知道报头的长度,用struck将报头长度这个数字转成固定长度:4个字节
head_len_bytes=struct.pack('i',len(head_bytes)) #这4个字节里只包含了一个数字,该数字是报头的长度

#客户端开始发送
conn.send(head_len_bytes) #先发报头的长度,4个bytes
conn.send(head_bytes) #再发报头的字节格式
conn.sendall(文件内容) #然后发真实内容的字节格式

#服务端开始接收
head_len_bytes=s.recv(4) #先收报头4个bytes,得到报头长度的字节格式
x=struct.unpack('i',head_len_bytes)[0] #提取报头的长度

head_bytes=s.recv(x) #按照报头长度x,收取报头的bytes格式
header=json.loads(json.dumps(header)) #提取报头

#最后根据报头的内容提取真实的数据,比如
real_data_len=s.recv(header['file_size'])
s.recv(real_data_len)
```
### 解决代码
##### server端
```
import  socket
import  subprocess
import struct
import  json
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('127.0.0.1',8080))
s.listen(5)

while True:
    conn, client_addr = s.accept()
    print('客户端的连接为%s' %conn)

    while True:
       try:
           cmd = conn.recv(1024)
           if not cmd: break
           print('客户端发来的命令为：%s' %cmd.decode('gbk'))
           res=subprocess.Popen(cmd.decode('gbk'),
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
           data=res.stdout.read()+res.stderr.read()
           if not data:break

           #制作报头
           header_dic={'total_lenth':len(data),'md5':None}
           header_json=json.dumps(header_dic)
           header_bytes=header_json.encode('utf8')

           #先发送报头的长度
           conn.send(struct.pack('i',len(header_bytes)))

           #再发送报头的内容
           conn.send(header_bytes)

           #再发送真实数据
           conn.send(data)
           
       except Exception as e:
           break
    conn.close()

s.close()
```
##### client端
```
import  socket
import  subprocess
import struct
import json
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.connect(('127.0.0.1',8080))

while True:
    cmd=input('输入命令>>:').strip()
    if not cmd:continue
    if cmd=='exit':break
    s.send(cmd.encode('utf8'))

    #先接收报头的长度
    struct_res=s.recv(4) #b'"\x00\x00\x00'
    header_size = struct.unpack('i', struct_res)[0] #34

    #再收报头
    header_bytes=s.recv(header_size).decode('gbk')
    header_json=json.loads(header_bytes)#{"total_lenth": 1677, "md5": null}
    data_lenth=header_json['total_lenth'] #接收内容的长度

    #再接收命令的执行结果
    recv_lenth=0
    data=b''
    while recv_lenth < data_lenth:
        recv_data=s.recv(1024)
        recv_lenth+=len(recv_data)
        data+=recv_data

    #打印结果
    print(data.decode('gbk'))
s.close()
```
# sockerserver实现并发
使用socketserver这个模块实现服务端并发，每当一个客户端来连接服务端的时候，服务端就开启一个线程（或者一个进程）来响应客户端的请求，以达到并发的效果，所以只在服务端的代码上做文章，客户端不用动
##### server端
```
class MyTcphandler(socketserver.BaseRequestHandler):
    def handle(self):  #这个函数的名字不要变
        while True: #通信循环
            data=self.request.recv(1024)
            self.request.send(data.upper())
if __name__ == '__main__':
    #取代链接循环
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8080),MyTcphandler)  #链接循环
    server.serve_forever() #链接循环  并实现并发的效果  人家已经给写好了

'''
需要变的就是ip  端口 以及收发的内容
函数名字不要变
'''
```
##### client端
```
import socket
phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
phone.connect(('127.0.0.1',8080))

while True:
    msg=input('>>: ').strip()
    if not msg:continue
    phone.send(msg.encode('utf-8'))
    server_data=phone.recv(1024)
    print(server_data.decode('utf-8'))

phone.close()
```
# 认证客户端的链接合法性
老师讲的例子   
如果你想在分布式系统中实现一个简单的客户端链接认证功能，又不像SSL那么复杂，那么利用hmac+加盐的方式来实现
##### server端
```
from socket import *
import hmac,os

secret_key=b'xxxxx'
def conn_auth(conn):
    '''
    认证客户端链接
    :param conn:
    :return:
    '''
    print('开始验证新链接的合法性')
    msg=os.urandom(32)
    conn.sendall(msg)
    h=hmac.new(secret_key,msg)
    digest=h.digest()
    respone=conn.recv(len(digest))
    return hmac.compare_digest(respone,digest)

def data_handler(conn,bufsize=1024):
    if not conn_auth(conn):
        print('该链接不合法,关闭')
        conn.close()
        return
    print('链接合法,开始通信')
    while True:
        data=conn.recv(bufsize)
        if not data:break
        conn.sendall(data.upper())

def server_handler(ip_port,bufsize,backlog=5):
    '''
    只处理链接
    :param ip_port:
    :return:
    '''
    tcp_socket_server=socket(AF_INET,SOCK_STREAM)
    tcp_socket_server.bind(ip_port)
    tcp_socket_server.listen(backlog)
    while True:
        conn,addr=tcp_socket_server.accept()
        print('新连接[%s:%s]' %(addr[0],addr[1]))
        data_handler(conn,bufsize)

if __name__ == '__main__':
    ip_port=('127.0.0.1',9999)
    bufsize=1024
    server_handler(ip_port,bufsize)
```
##### client端-合法
```
from socket import *
import hmac,os

secret_key=b'xxxxx'
def conn_auth(conn):
    '''
    验证客户端到服务器的链接
    :param conn:
    :return:
    '''
    msg=conn.recv(32)
    h=hmac.new(secret_key,msg)
    digest=h.digest()
    conn.sendall(digest)

def client_handler(ip_port,bufsize=1024):
    tcp_socket_client=socket(AF_INET,SOCK_STREAM)
    tcp_socket_client.connect(ip_port)

    conn_auth(tcp_socket_client)

    while True:
        data=input('>>: ').strip()
        if not data:continue
        if data == 'quit':break

        tcp_socket_client.sendall(data.encode('utf-8'))
        respone=tcp_socket_client.recv(bufsize)
        print(respone.decode('utf-8'))
    tcp_socket_client.close()

if __name__ == '__main__':
    ip_port=('127.0.0.1',9999)
    bufsize=1024
    client_handler(ip_port,bufsize)
```
##### client端(非法:不知道加密方式)
```
from socket import *

def client_handler(ip_port,bufsize=1024):
    tcp_socket_client=socket(AF_INET,SOCK_STREAM)
    tcp_socket_client.connect(ip_port)

    while True:
        data=input('>>: ').strip()
        if not data:continue
        if data == 'quit':break

        tcp_socket_client.sendall(data.encode('utf-8'))
        respone=tcp_socket_client.recv(bufsize)
        print(respone.decode('utf-8'))
    tcp_socket_client.close()

if __name__ == '__main__':
    ip_port=('127.0.0.1',9999)
    bufsize=1024
    client_handler(ip_port,bufsize)
```
##### client端(非法:不知道secret_key)
```
from socket import *
import hmac,os

secret_key=b'linhaifeng bang bang bang1111'
def conn_auth(conn):
    '''
    验证客户端到服务器的链接
    :param conn:
    :return:
    '''
    msg=conn.recv(32)
    h=hmac.new(secret_key,msg)
    digest=h.digest()
    conn.sendall(digest)

def client_handler(ip_port,bufsize=1024):
    tcp_socket_client=socket(AF_INET,SOCK_STREAM)
    tcp_socket_client.connect(ip_port)

    conn_auth(tcp_socket_client)

    while True:
        data=input('>>: ').strip()
        if not data:continue
        if data == 'quit':break

        tcp_socket_client.sendall(data.encode('utf-8'))
        respone=tcp_socket_client.recv(bufsize)
        print(respone.decode('utf-8'))
    tcp_socket_client.close()

if __name__ == '__main__':
    ip_port=('127.0.0.1',9999)
    bufsize=1024
    client_handler(ip_port,bufsize)
```