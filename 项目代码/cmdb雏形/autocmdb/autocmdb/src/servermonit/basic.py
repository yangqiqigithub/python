#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from lib.response import BaseResponse
from src.servermonit.base import BasePlugin
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

    def linux(self):
        response = BaseResponse()
        try:
            ret = {
                'hostname': self.os_hostname(),
                'ip':self.ip

            }
            response.data = ret
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response

