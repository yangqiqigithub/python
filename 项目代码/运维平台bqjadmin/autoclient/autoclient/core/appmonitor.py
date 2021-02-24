import traceback
from lib.response import BaseResponse
from core.base import Base
from config.settings import app_monitor_config
import subprocess
import psutil
import time
class AppMoni(Base):
    def get_appmoni(self):
        response=BaseResponse()
        try:
            # appmonitor_dict
            appmonitor_dict = {
                'flag': '2',
                'mongod': [],
                'redis-server': [],
                'java': [],
                'mysqld': [],
                'python3': [],
                'nginx': [],
                'postgres':[]
            }

            for k, v in app_monitor_config.items():
                appname = k
                port_list = v
                for port in port_list:
                    cmd = 'netstat -tnlp |grep' + ' ' + appname + ' ' + '|' + 'grep' + ' ' + port
                    status, output = subprocess.getstatusoutput(cmd)
                    if status == 0:
                        l = output.split('/')[0].split(' ')
                        pid = int(l[len(l) - 1])
                        p = psutil.Process(pid)
                        name = p.name() + port  # 服务名称和端口组合为服务名称 mysql3306
                        status = p.status()  # 服务状态
                        create_time = int(p.create_time())
                        life_time = int(time.time()) - create_time  # 服务运行时间
                        cpu_util = p.cpu_percent()  # cpu使用率
                        memory_total_size = round(psutil.virtual_memory().total / 1024 / 1024, 2)  # 系统内存总大小 MB
                        memory_util = round(p.memory_percent(), 2)  # 内存使用率
                        if int(psutil.swap_memory().total) == 0 or int(p.memory_full_info().swap) == 0:
                            swap_total_size = 0
                            swap_used_size = 0
                        else:
                            swap_total_size = round(psutil.swap_memory().total / 1024 / 1024, 2)  # 系统swap总大小MB
                            swap_used_size = round(p.memory_full_info().swap / 1024 / 1024, 2)  # 程序使用swap大小MB

                        disk_read_mb = round(p.io_counters().read_bytes / 1024 / 1024 / life_time, 2)  # 磁盘读流量MB
                        disk_write_mb = round(p.io_counters().write_bytes / 1024 / 1024 / life_time, 2)  # 磁盘写流量MB
                        threads_count = p.num_threads()  # 开启的线程数
                        connections_list = []
                        for i in p.connections():
                            if i.status == 'ESTABLISHED':
                                connections_list.append(i)
                        connections_count = len(connections_list)  # 建立ESTABLISHED链接的进程数
                        appinfo = {
                                   'alive':'1',
                                    'name': name, 'status': status, 'pid': pid, 'life_time': life_time,
                                   'cpu_util': cpu_util,
                                   'memory_total_size': memory_total_size, 'memory_util': memory_util,
                                   'swap_total_size': swap_total_size,
                                   'swap_used_size': swap_used_size, 'disk_read_mb': disk_read_mb,
                                   'disk_wirte_mb': disk_write_mb,
                                   'threads_count': threads_count, 'connections_count': connections_count}

                        appmonitor_dict[appname].append(appinfo)
                    else:  # 当服务程序死了或者命令执行错误 status=1
                        alive_cmd = cmd + ' ' + '| wc -l '
                        s,o = subprocess.getstatusoutput(alive_cmd)
                        if s==0:
                            if o=='0':
                                appinfo = {'alive': '0','name':appname+port}
                                appmonitor_dict[appname].append(appinfo)
                        else:
                            msg = "主机-%s-%s抓取程序监控信息失败,netstat命令执行错误,class AppMoni出错,%s"
                            self.logger.log(msg % (self.hostname, self.ip, traceback.format_exc()), False)
                            response.status = False
                            response.error = msg % (self.hostname, self.ip, traceback.format_exc())
            response.data=appmonitor_dict
        except Exception as e:
            msg = "主机-%s-%s抓取程序监控信息失败,class AppMoni出错,%s"
            self.logger.log(msg % (self.hostname, self.ip, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, self.ip, traceback.format_exc())
        return response

