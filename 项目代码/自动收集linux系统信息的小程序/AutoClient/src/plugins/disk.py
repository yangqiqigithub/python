#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
from .base import BasePlugin
from lib.response import BaseResponse
from lib.common import  Bytes_GB,Bytes_KB,ms_s
import psutil
import re

class DiskPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            per_part_info_dict = {}
            for partinfo in psutil.disk_partitions():
                k = str(partinfo.device)
                per_part_info_dict.setdefault(k, {'device': partinfo.device,
                                                  'mountpoint': partinfo.mountpoint,
                                                  'fstype': partinfo.fstype})

            for k, v in per_part_info_dict.items():
                total_GB = Bytes_GB(psutil.disk_usage(v.get('mountpoint')).total)
                used_GB = Bytes_GB(psutil.disk_usage(v.get('mountpoint')).used)
                percent = psutil.disk_usage(v.get('mountpoint')).percent

                per_part_info_dict[k].setdefault('total_GB', total_GB)
                per_part_info_dict[k].setdefault('used_GB', used_GB)
                per_part_info_dict[k].setdefault('percent', percent)

            dic = {}
            for k, v in psutil.disk_io_counters(perdisk=True).items():

                per_disk_read_count = v.read_count
                per_disk_write_count = v.write_count
                per_disk_read_kb = Bytes_KB(v.read_bytes)
                per_disk_write_kb = Bytes_KB(v.write_bytes)
                per_disk_read_time_s = ms_s(v.read_time)
                per_disk_write_time_s = ms_s(v.write_time)

                try:
                    dic.setdefault(k, {
                        'r/s': per_disk_read_count // per_disk_read_time_s,
                        'w/s': per_disk_write_count // per_disk_write_time_s,
                        'rKB/s': per_disk_read_kb // per_disk_read_time_s,
                        'wKB/s': per_disk_write_kb // per_disk_write_time_s,
                    })
                except Exception as e:
                    pass

            for k, v in per_part_info_dict.items():
                new_k = ''.join(re.findall('[a-z]{3}\d', k))
                per_part_info_dict[k].update(dic[new_k])
            response.data = per_part_info_dict
        except Exception as e:
            msg = "%s linux DiskPlugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response


