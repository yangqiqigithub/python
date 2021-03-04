#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.log import Logger


class BasePlugin(object):
    def __init__(self):
        self.logger = Logger()
        self.hostname=self.hostname()


    def hostname(self):
        """
        获取主机名
        :return:
        """
        output = self.exec_shell_cmd('hostname')
        return output.strip()




    def exec_shell_cmd(self, cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output


    def linux(self):
        raise Exception('You must implement linux method.')
