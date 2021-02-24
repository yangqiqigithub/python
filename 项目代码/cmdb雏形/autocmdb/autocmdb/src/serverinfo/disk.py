#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import traceback
from .base import BasePlugin
from lib.response import BaseResponse
from lib.common import clear_list
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import traceback
from .base import BasePlugin
from lib.response import BaseResponse


class DiskPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            stdin, stdout, stderr = self.ssh.exec_command('df -hT')
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
        diskinfo = content.split('\n')
        response = {}
        for i in diskinfo:
            l = clear_list(i.strip().split(' '))
            disk_name = l[0]
            disk_type = l[1]
            disk_size = l[2]
            disk_used = l[3]
            disk_aval = l[4]
            s = re.findall('/\w{3}/\w{3}', disk_name)  # 是否匹配 /dev/sdb1 /dev/vdb 这样的格式
            if s:
                response.setdefault(disk_name, {
                    'name': disk_name,
                    'type': disk_type,
                    'size': disk_size,
                    'used': disk_used,
                    'aval': disk_aval
                })
        return response


