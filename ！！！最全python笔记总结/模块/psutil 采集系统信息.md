### cpu
```
import psutil
#物理个数 2
cpu_physical_count=psutil.cpu_count(logical=False)

#逻辑个数 4
cpu_core_count=psutil.cpu_count()

#负载 (0.0, 0.0, 0.0)
cpu_avg_load_tuple=psutil.getloadavg()

#cpu 总的cpu使用率
cpu_total_util=psutil.cpu_percent(interval=1)

#每核cpu的使用率 [21.9, 14.1, 42.2, 24.6]
cpu_per_util_list=psutil.cpu_percent(interval=1,percpu=True)

#每核CPU的具体情况
for i in psutil.cpu_times_percent(percpu=True,interval=1):
    print(i)
'''
scputimes(user=11.9, system=20.9, idle=62.7, interrupt=0.0, dpc=4.5)
scputimes(user=9.2, system=10.8, idle=78.5, interrupt=1.5, dpc=0.0)
scputimes(user=10.9, system=15.6, idle=73.4, interrupt=0.0, dpc=0.0)
scputimes(user=15.1, system=17.8, idle=54.8, interrupt=1.4, dpc=11.0)
```
### 内存
```
import  psutil

#采集内存信息
vm=psutil.virtual_memory()
'''
svmem(total=8010076160, available=3027079168, percent=62.2, used=4982996992, free=3027079168) 单位是bytes
'''
#采集交换内存信息 
sm=psutil.swap_memory()
'''
sswap(total=14452527104, used=6798229504, free=7654297600, percent=47.0, sin=0, sout=0) 单位是字节
'''
```
### 硬盘
```
import  psutil

#查看所有磁盘总的io情况
print(psutil.disk_io_counters())
'''
sdiskio(read_count=349135537, write_count=173350456, read_bytes=45840149228544, write_bytes=41993328918528, read_time=1642928562, write_time=3234784887, read_merged_count=42249, write_merged_count=55960610, busy_time=1015060410)
'''

#查看每块磁盘，每个分区的io情况
print(psutil.disk_io_counters(perdisk=True))
'''
{
   'vda': sdiskio(read_count = 11675971, write_count = 30908249, read_bytes = 603276977152, write_bytes = 592860377088, read_time = 174826885, write_time = 268118871, read_merged_count = 7032, write_merged_count = 30894855, busy_time = 40317910),
   'vda1': sdiskio(read_count = 11675878, write_count = 30765130, read_bytes = 603274572800, write_bytes = 592860377088, read_time = 174826391, write_time = 268110167, read_merged_count = 7032, write_merged_count = 30894855, busy_time = 40311299),
   'vdb': sdiskio(read_count = 213974379, write_count = 115117376, read_bytes = 31540307026944, write_bytes = 28416783298560, read_time = 1334811200, write_time = 1189838637, read_merged_count = 29354, write_merged_count = 23885045, busy_time = 697986483),
   'vdb1': sdiskio(read_count = 213974343, write_count = 113944688, read_bytes = 31540305675264, write_bytes = 28416783298560, read_time = 1334811046, write_time = 1189452023, read_merged_count = 29354, write_merged_count = 23885045, busy_time = 697932651),
   'sr0': sdiskio(read_count = 0, write_count = 0, read_bytes = 0, write_bytes = 0, read_time = 0, write_time = 0, read_merged_count = 0, write_merged_count = 0, busy_time = 0),
   'vdc': sdiskio(read_count = 123485187, write_count = 27324831, read_bytes = 13696565224448, write_bytes = 12983685242880, read_time = 133290477, write_time = 1776827379, read_merged_count = 5863, write_merged_count = 1180710, busy_time = 276756017),
   'vdc1': sdiskio(read_count = 123485105, write_count = 27323664, read_bytes = 13696562783232, write_bytes = 12983685238784, read_time = 133290404, write_time = 1776826739, read_merged_count = 5863, write_merged_count = 1180710, busy_time = 276755374)
}

'''
#查看磁盘分区情况
print(psutil.disk_partitions())
'''
[sdiskpart(device='/dev/vda1', mountpoint='/', fstype='ext4', opts='rw,relatime,data=ordered'), sdiskpart(device='/dev/vdb1', mountpoint='/home/bak', fstype='ext4', opts='rw,relatime,data=ordered'), sdiskpart(device='/dev/vdc1', mountpoint='/backup', fstype='ext4', opts='rw,relatime,data=ordered')]
'''
```
### 网络
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang
import  psutil

#查看网络总的io
print(psutil.net_io_counters())
'''
snetio(bytes_sent=33867659755817, bytes_recv=44033153132340, packets_sent=7124106374, packets_recv=34191094132, errin=0, errout=0, dropin=0, dropout=0)
'''
#每块网卡地址信息
print(psutil.net_if_addrs())
'''
{
   'lo': [snicaddr(family = < AddressFamily.AF_INET: 2 > , address = '127.0.0.1', netmask = '255.0.0.0', broadcast = None, ptp = None), snicaddr(family = < AddressFamily.AF_PACKET: 17 > , address = '00:00:00:00:00:00', netmask = None, broadcast = None, ptp = None)],
   'eth0': [snicaddr(family = < AddressFamily.AF_INET: 2 > , address = '172.17.133.181', netmask = '255.255.240.0', broadcast = '172.17.143.255', ptp = None), snicaddr(family = < AddressFamily.AF_PACKET: 17 > , address = '00:16:3e:06:57:91', netmask = None, broadcast = 'ff:ff:ff:ff:ff:ff', ptp = None)],
   'docker0': [snicaddr(family = < AddressFamily.AF_INET: 2 > , address = '172.18.0.1', netmask = '255.255.0.0', broadcast = '172.18.255.255', ptp = None), snicaddr(family = < AddressFamily.AF_PACKET: 17 > , address = '02:42:87:88:12:06', netmask = None, broadcast = 'ff:ff:ff:ff:ff:ff', ptp = None)],
   'docker_gwbridge': [snicaddr(family = < AddressFamily.AF_INET: 2 > , address = '172.19.0.1', netmask = '255.255.0.0', broadcast = '172.19.255.255', ptp = None), snicaddr(family = < AddressFamily.AF_PACKET: 17 > , address = '02:42:1f:90:df:c4', netmask = None, broadcast = 'ff:ff:ff:ff:ff:ff', ptp = None)]
}
'''
#每块网卡状态信息
print(psutil.net_if_stats())
'''
{'eth0': snicstats(isup=True, duplex=<NicDuplex.NIC_DUPLEX_UNKNOWN: 0>, speed=0, mtu=1500), 'lo': snicstats(isup=True, duplex=<NicDuplex.NIC_DUPLEX_UNKNOWN: 0>, speed=0, mtu=65536), 'docker_gwbridge': snicstats(isup=True, duplex=<NicDuplex.NIC_DUPLEX_UNKNOWN: 0>, speed=0, mtu=1500), 'docker0': snicstats(isup=True, duplex=<NicDuplex.NIC_DUPLEX_UNKNOWN: 0>, speed=0, mtu=1500)}
'''
#查看当前的网络连接
print(psutil.net_connections())
'''
[
sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='127.0.0.1', port=32000), raddr=addr(ip='127.0.0.1', port=55404), status='CLOSE_WAIT', pid=None),

sconn(fd=5, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='172.17.133.181', port=52098), raddr=addr(ip='172.17.134.130', port=9266), status='ESTABLISHED', pid=7630), sconn(fd=17, family=<AddressFamily.AF_INET6: 10>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='::', port=123), raddr=(), status='NONE', pid=27881), 

]
'''
```
### 登录用户
```
import  psutil
#当前登录的用户们们
print(psutil.users())
'''
[suser(name='Administrator', terminal=None, host='0.4.0.0', started=1563445128.0, pid=None)]
'''
```
### 开机时间
```
import  psutil,datetime
#显示开机时间
print(psutil.boot_time()) #1558941745.0
boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S') #时间转换
```
### 进程管理
```
import  psutil
#查看当前都有哪些进程
print(psutil.pids()) #[0, 4, 96, 212, 380, 532, 576, 672, 700, 816, 832]
#查看某个进程是否存在
print(psutil.pid_exists(96)) #True

p=psutil.Process(816) #根据pid实例化一个进程对象
#进程名字
print('name',p.name()) #vsftpd
#进程bin路径
print('exe',p.exe()) #/usr/sbin/vsftpd
#进程工作目录绝对路径
print('cwd',p.cwd()) #/usr/local/vsftp
#进程状态
print('status',p.status()) #sleeping
#进程创建时间
print('create_time',p.create_time()) #1540950455.14
#进程uid信息
print('uids',p.uids()) #puids(real=0, effective=0, saved=0)
#进程gid信息
print('gids',p.gids()) # pgids(real=0, effective=0, saved=0)

进程cpu时间信息
print('cpu_times()',p.cpu_times)
# pcputimes(user=0.02, system=0.26, children_user=1.36, children_system=2.83)

#进程cpu利用率
print('cpu_percent',p.cpu_percent()) #0.1

#进程cpu亲和度 如要设置，将cpu的号作为作为参数即可
print('cpu_affinity',p.cpu_affinity()) #[0, 1, 2, 3]

print('cpu_num',p.cpu_num()) # 2

print('memory_info',p.memory_info())
#pmem(rss=688128, vms=54538240, shared=102400, text=159744, lib=0, data=462848, dirty=0)

print('memory_full_info',p.memory_full_info())
# pfullmem(rss=688128, vms=54538240, shared=102400, text=159744, lib=0, data=462848, dirty=0, uss=614400, pss=616448, swap=0)

print('memory_info_ex',p.memory_info_ex)
# <bound method Process.memory_info_ex of psutil.Process(pid=25445, name='vsftpd', started='2018-10-31 09:47:35')>

print('memory_percent',p.memory_percent()) # 0.008389307827174267

print('io_counters',p.io_counters())
#pio(read_count=63450, write_count=41896, read_bytes=1575538688, write_bytes=60854272, read_chars=87372163, write_chars=60581613)

print('connections',p.connections())
#[pconn(fd=3, family=<AddressFamily.AF_INET6: 10>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='::', port=21), raddr=(), status='LISTEN')]

#进程开启的线程数
print('num_threads',p.num_threads()) #1
```