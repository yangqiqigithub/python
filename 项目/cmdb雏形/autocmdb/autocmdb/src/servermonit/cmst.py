#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import traceback
from .base import BasePlugin
from lib.response import BaseResponse
import re
from lib.common import clear_list

class CmstPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            stdin, stdout, stderr = self.ssh.exec_command("top -bsin1")
            output = stdout.read().decode('gbk').strip()
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux cmst plugin error: %s"
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
        output=content
        host_dict = {"tasks": {},
                     "loadavg": {},
                     "cpu": {},
                     "mem": {},
                     "swap": {},
                     }

        loadavg_list = re.findall('load average:\s\d+.\d+,\s\d+.\d+,\s\d+.\d+', output)[0].split(':')
        l = []
        for i in loadavg_list[1].split(','):
            l.append(i.strip())
        host_dict["loadavg"] = l

        tasks_list = re.findall('Tasks:.*', output)[0].split(':')
        for i in tasks_list[1].split(','):
            host_dict["tasks"].setdefault(clear_list(i.split(' '))[1], clear_list(i.split(' '))[0])

        cpu_list = re.findall('%Cpu\(s\):.*', output)[0].split(':')
        for i in cpu_list[1].split(','):
            host_dict["cpu"].setdefault(clear_list(i.split(' '))[1], clear_list(i.split(' '))[0])
        host_dict["cpu"].setdefault('util', round(100 - float(host_dict["cpu"]['id']), 2))

        mem_list = re.findall('KiB Mem.*', output)[0].split(':')
        for i in mem_list[1].split(','):
            host_dict["mem"].setdefault(clear_list(i.split(' '))[1], round(int(clear_list(i.split(' '))[0]) / 1001))
        host_dict["mem"].setdefault("util", round(host_dict["mem"]['used'] / host_dict["mem"]['total'] * 100, 2))

        swap_list = re.findall('KiB Swap:.*', output)[0].split(':')
        for i in swap_list[1].split(','):
            if len(clear_list(i.split(' '))) == 2:
                host_dict["swap"].setdefault(clear_list(i.split(' '))[1],
                                             round(int(clear_list(i.split(' '))[0]) / 1001))
            else:
                for j in i.split('.'):
                    host_dict["swap"].setdefault(clear_list(j.split(' '))[1],
                                                 round(int(clear_list(j.split(' '))[0]) / 1001))
            if host_dict['swap']['total'] == 0:
                host_dict["swap"].setdefault("util", 0)
            else:
                host_dict["swap"].setdefault("util", round(host_dict['swap']['used'] / host_dict['swap']['total'], 2))

        if int(host_dict['swap']['total'])==0:
            host_dict['swap']['total']=host_dict['swap']['avail']
        return host_dict

