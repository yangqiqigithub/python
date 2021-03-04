import  psutil
import traceback
from lib.response import BaseResponse
from core.base import Base
class ServerMoni(Base):
    def get_servermoni(self):
        response=BaseResponse()
        try:
            # 系统负载
            load_5m = round(psutil.getloadavg()[0], 3)
            load_10m = round(psutil.getloadavg()[1], 3)
            load_15m = round(psutil.getloadavg()[2], 3)
            # cpu利用率
            cpu_util = psutil.cpu_percent(interval=1)
            # 内存利用率
            memory_util = psutil.virtual_memory().percent
            # swap利用率
            swap_util = psutil.swap_memory().percent
            # 磁盘流量
            import re
            disk_list=[]
            for disk in psutil.disk_partitions():
                name = re.findall('\w+', disk.device)[1]
                space_util = psutil.disk_usage(disk.mountpoint).percent
                obj = psutil.disk_io_counters(perdisk=True).get(name)
                if obj:
                    rmbs = round(obj.read_bytes / 1024 / 1024 / obj.read_time, 3)
                    wmbs = round(obj.write_bytes / 1024 / 1024 / obj.write_time, 3)
                else:
                    rmbs = 0
                    wmbs = 0
                disk_list.append({"name":name,"space_util":space_util,"rmbs":rmbs,"wmbs":wmbs})
            # 网卡流量
            uptime = int(psutil.boot_time()) #系统运行时间
            sentmbs = round(psutil.net_io_counters().bytes_sent / 1024 / 1024 / uptime, 3)
            recvmbs = round(psutil.net_io_counters().bytes_recv / 1024 / 1024 / uptime, 3)

            servermoni_dict={
                "flag":"1",
                "load":{
                    "load_5m":load_5m,
                    "load_10m":load_10m,
                    "load_15m":load_15m
                },
                "cpu_util":cpu_util,
                "memory_util":memory_util,
                "swap_util":swap_util,
                "disk_list":disk_list,
                "net_flow":{
                    "sentmbs":sentmbs,
                    "recvmbs":recvmbs
                },
                "uptime":uptime,
            }
            response.data=servermoni_dict
        except Exception as e:
            msg = "主机-%s抓取系统监控信息失败,class ServerMoni出错,%s"
            self.logger.log(msg % (self.hostname,self.ip, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname,self.ip, traceback.format_exc())
        return response

