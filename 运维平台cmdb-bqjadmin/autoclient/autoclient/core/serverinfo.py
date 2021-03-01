import  psutil

import traceback
from lib.response import BaseResponse
from core.base import Base
class ServerInfo(Base):
    def get_serverinfo(self):
        response=BaseResponse()
        try:
            #内存总大小
            memory_total_size=round(psutil.virtual_memory().total/1024/1024/1024,2)
            #交换内存总大小
            swap_total_size=round(psutil.swap_memory().total/1024/1024/1024,2)
            #cpu核数
            cpu_cores=psutil.cpu_count()
            #网卡信息
            net_list=[]
            for name,v in psutil.net_if_addrs().items():
                ip=v[0].address
                netmask=v[0].netmask
                broadcast=v[0].broadcast
                if all((ip,netmask,broadcast)):
                    net_list.append({"name":name,"ip":ip,"netmask":netmask,"broadcast":broadcast})
            #磁盘信息
            disk_list=[]
            for disk in psutil.disk_partitions():
                disk_list.append({"name":disk.device,"total_size":round(psutil.disk_usage(disk.mountpoint).total/1024/1024/1024,2)})

            #主机运行状态
            status='running' ##目前是写死的 后期得考虑如何检测主机是否在运行中
            serverinfo_dict={
                             "flag":"0",
                             "hostname":self.hostname,
                             "version":self.version,
                             "cpu_cores":cpu_cores,
                             "memory_total_size":memory_total_size,
                             "swap_total_size":swap_total_size,
                             "net_list":net_list,
                             "disk_list":disk_list,
                             "status":status}
            response.data=serverinfo_dict

        except Exception as e:
            msg="主机-%s-%s抓取系统信息失败,class ServerInfo出错,%s"
            self.logger.log(msg %(self.hostname,self.ip,traceback.format_exc()),False)
            response.status=False
            response.error=msg %(self.hostname,self.ip,traceback.format_exc())
        return response



