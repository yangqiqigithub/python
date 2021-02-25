#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from .base import BasePlugin
from lib.response import BaseResponse
from lib.common import clear_list

class NicPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            stdin, stdout, stderr = self.ssh.exec_command("sar -n DEV 1 1 |grep Average |grep -v lo")
            output = stdout.read().decode('gbk').strip()
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux cpu plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    @staticmethod
    def parse(content):
        """
        解析shell命令返回结果
        :param content: shell 命令结果
        :return:解析后的结果
        """
        output = content.splitlines()
        li = []
        nic_dict = {}
        for i in output:
            li.append(clear_list(i.split(' ')))

        for j in li[1:len(li)]:
            if j[1] == 'eth0':
                e = zip(li[0], j)
                for i in e:
                    nic_dict.setdefault(i[0].lower(), i[1])
        del nic_dict["average:"]
        return nic_dict
 # {'iface': 'eth0', 'rxpck/s': '13.00', 'txpck/s': '11.00', 'rxkb/s': '38.68', 'txkb/s': '0.75', 'rxcmp/s': '0.00', 'txcmp/s': '0.00', 'rxmcst/s': '0.00'}






