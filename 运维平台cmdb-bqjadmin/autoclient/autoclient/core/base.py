from lib.log import Logger
import psutil

class Base(object):

    def __init__(self):
        self.logger=Logger()
        self.hostname=self.hostname()
        self.version=self.version()

    def exec_shell_cmd(self,cmd):
        import subprocess
        status,output=subprocess.getstatusoutput(cmd)
        if status==0:
            output=output
        else:
            output='none'
        return output

    def hostname(self):
        #主机名
        hostname=self.exec_shell_cmd('hostname')
        return hostname

    def ip(self):
        try:
            ip=psutil.net_if_addrs().get('eth0')[0].address
        except Exception as e:
            net_list = []
            for name, v in psutil.net_if_addrs().items():
                ip = v[0].address
                netmask = v[0].netmask
                broadcast = v[0].broadcast
                if all((ip, netmask, broadcast)):
                    net_list.append({"name": name, "ip": ip, "netmask": netmask, "broadcast": broadcast})
            ip=net_list[0]['ip']
        return ip

    def version(self):
        # 系统版本
        version='none'
        try:
            version = self.exec_shell_cmd('cat /etc/redhat-release')
        except  Exception as e:
            version = self.exec_shell_cmd('cat /etc/issue')
        return version



