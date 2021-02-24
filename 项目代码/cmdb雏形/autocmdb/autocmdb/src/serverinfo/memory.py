#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import traceback
from lib import convert
from .base import BasePlugin
from lib.response import BaseResponse
from lib.common import kb_GB

class MemoryPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            stdin, stdout, stderr = self.ssh.exec_command("cat /proc/meminfo")
            output = stdout.read().decode('gbk').strip()
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux memory plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    def parse(self, content):
        """
        解析shell命令返回结果
        :param content: shell 命令结果
        :return:解析后的结果
        """
        memeoryinfo_dict = {}
        available_keys=['MemTotal','MemFree', 'MemAvailable']
        for item in content.split('\n'):
            key = item.split(':')[0].strip()
            value = kb_GB(item.split(':')[1].strip())
            if key in available_keys:
                memeoryinfo_dict.setdefault(key, value)
        return memeoryinfo_dict
