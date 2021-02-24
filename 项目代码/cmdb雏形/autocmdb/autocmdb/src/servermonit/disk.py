#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from lib.common import clear_list
import traceback
from .base import BasePlugin
from lib.response import BaseResponse
from lib.common import all_GB

class DiskPlugin(BasePlugin):
    def exec_iostat(self):
        try:
            stdin, stdout, stderr = self.ssh.exec_command('iostat -x')
            output = stdout.read().decode('gbk').strip()
            dic = self.parse_iostat(output)
        except Exception as e:
            msg = "%s linux disk-iostat plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
        return dic

    @staticmethod
    def parse_iostat(content):
        output = content
        disk_device_list = []  # ['vda', 'vdb']
        disk_dict = {}
        disk_list = re.findall('[sv]d[a-z].*', output)
        name_list = clear_list(re.findall('Device:.*', output)[0].split(' '))
        for i in name_list:
            if i == 'Device:':
                name_list[name_list.index('Device:')] = 'device'
            else:
                name_list[0] = 'device'
        name_list[-1] = "io_util"
        for i in disk_list:
            data_list = clear_list(i.split(' '))
            disk_dict.setdefault(data_list[0], list(zip(name_list, data_list)))
            disk_device_list.append(data_list[0])

        for k, v in disk_dict.items():
            d = {}
            for i in v:
                d.setdefault(i[0], i[1])
            disk_dict[k] = d
        return disk_dict, disk_device_list

    def exec_dfht(self):
        try:
            stdin, stdout, stderr = self.ssh.exec_command('df -hT')
            output = stdout.read().decode('gbk').strip()
            device_list = self.exec_iostat()[1]
            dic = self.parse_dfht(output, device_list)
        except Exception as e:
            msg = "%s linux disk- df-HT plugin error: %s"
            # self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
        return dic

    @staticmethod
    def parse_dfht(content, device_list):
        output = content
        li = []
        for i in output.splitlines():
            l = clear_list(i.split(' '))

            if re.findall('[sv]d[a-z]', l[0]):
                if re.findall('[sv]d[a-z]', l[0])[0] in device_list:
                    total = all_GB(clear_list(i.split(' '))[2])
                    used = all_GB(clear_list(i.split(' '))[3])
                    aval = all_GB(clear_list(i.split(' '))[4])
                    size_util = clear_list(i.split(' '))[5].split('%')[0]
                    device_name = re.findall('[sv]d[a-z]', l[0])[0]
                    li.append({device_name: {"total": total, "used": used, "aval": aval, "size_util": size_util}})
            else:
                pass
        from collections import Counter
        end_data = {}
        for li_i in li:
            list_i_vues = list(li_i.values())[0]  # 获取vlues
            list_i = list(li_i.keys())[0]  # 获取key
            if list_i in end_data.keys():
                list_i_vues = {kk: int(yy) for kk, yy in list_i_vues.items()}
                end_data[list_i] = {kk: int(yy) for kk, yy in end_data[list_i].items()}
                X, Y = Counter(list_i_vues), Counter(end_data[list_i])
                end_data[list_i] = dict(X + Y)
            else:
                end_data.update(li_i)
        for k, v in end_data.items():
            v['size_util'] = int(v['used'] / v['total'] * 100)

        return end_data

    def linux(self):
        response = BaseResponse()
        try:
            disk_dict = self.exec_iostat()[0]
            end_data = self.exec_dfht()
            # print(disk_dict)
            # print(end_data)
            for k, v in disk_dict.items():
                disk_dict[k].setdefault("total", end_data[k]['total'])
                disk_dict[k].setdefault("used", end_data[k]['used'])
                disk_dict[k].setdefault("aval", end_data[k]['aval'])
                disk_dict[k].setdefault("size_util", end_data[k]['size_util'])

            response.data = disk_dict
        except Exception as e:
            msg = "%s linux disk plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response



