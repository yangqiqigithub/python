#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import traceback
from .base import BasePlugin
from lib.response import BaseResponse
import psutil

class CpuPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:

            # 物理个数 2
            cpu_physical_count = psutil.cpu_count(logical=False)

            # 逻辑个数 4
            cpu_core_count = psutil.cpu_count()

            # 负载 (0.0, 0.0, 0.0)
            cpu_load_tuple = psutil.getloadavg()

            #cpu 总的cpu使用率 0.8
            cpu_total_util = psutil.cpu_percent(interval=1)

            response.data = {"cpu_physical_count":cpu_physical_count,
                             "cpu_core_count":cpu_core_count,
                             "cpu_load_tuple":cpu_load_tuple,
                             "cpu_total_util":cpu_total_util}
        except Exception as e:
            msg = "%s linux CpuPlugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

