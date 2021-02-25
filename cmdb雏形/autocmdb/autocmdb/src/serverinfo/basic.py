#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from lib.response import BaseResponse
from src.serverinfo.base import BasePlugin
from lib.common import create_unique_id
class BasicPlugin(BasePlugin):

    def os_hostname(self):
        """
        获取系统版本
        :return:
        """
        stdin, stdout, stderr = self.ssh.exec_command('hostname')
        hostname = stdout.read().decode('gbk').strip()

        return hostname

    def os_version(self):
        """
        获取主机名
        :return:
        """
        stdin, stdout, stderr = self.ssh.exec_command('cat /etc/redhat-release')
        version = stdout.read().decode('gbk').strip()
        return version

    def get_unique_id(self):
        '''
        获取主机唯一id
        :return:
        '''
        stdin, stdout, stderr = self.ssh.exec_command('cat /etc/unique_id')
        err_msg = stderr.read().decode('gbk')
        unique_id = stdout.read().decode('gbk').strip()
        if err_msg:
            if 'such' in err_msg:
                unique_id = create_unique_id().strip()
                echo_cmd = "echo" + " " + unique_id + " " + ">" + " " + "/etc/unique_id"
                stdin, stdout, stderr = self.ssh.exec_command('touch /etc/unique_id')
                stdin1, stdout1, stderr1 = self.ssh.exec_command(echo_cmd)
                return unique_id
        else:
            return unique_id


    def linux(self):
        response = BaseResponse()
        try:
            ret = {
                'os_version': self.os_version(),
                'hostname': self.os_hostname(),
                'unique_id':self.get_unique_id(),
                'conninfo':self.host_dict
            }
            response.data = ret
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response

