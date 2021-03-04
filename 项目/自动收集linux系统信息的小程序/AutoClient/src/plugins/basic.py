#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from .base import BasePlugin
from lib.response import BaseResponse


class BasicPlugin(BasePlugin):

    def version(self):
        """
        获取系统版本
        :return:
        """
        output = self.exec_shell_cmd('cat /etc/redhat-release')
        result = output.strip().split('\n')[0]
        return result



    def linux(self):
        response = BaseResponse()
        try:
            ret = {
                'version': self.version(),
                'hostname': self.hostname,
            }
            response.data = ret
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response

