#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import traceback
from .base import BasePlugin
from lib.response import BaseResponse
import psutil
from lib.common import  Bytes_GB

class MemoryPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            vm = psutil.virtual_memory()
            response.data = {"total":Bytes_GB(vm.total),"used":Bytes_GB(vm.used),"percent":vm.percent}
        except Exception as e:
            msg = "%s linux MemoryPlugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response


