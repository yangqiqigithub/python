#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang


import traceback
from .base import BasePlugin
from lib.response import BaseResponse
import psutil
from lib.common import Bytes_GB


class SwapPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            sm=psutil.swap_memory()
            response.data = {"total": Bytes_GB(sm.total), "used": Bytes_GB(sm.used), "percent": sm.percent}
        except Exception as e:
            msg = "%s linux SwapPlugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

