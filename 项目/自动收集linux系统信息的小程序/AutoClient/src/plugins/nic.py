#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
from .base import BasePlugin
from lib.response import BaseResponse
import psutil,time
from  lib.common import Bytes_KB
class NicPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:

            uptime=int(time.time()) - int(psutil.boot_time())
            nicflow = psutil.net_io_counters()
            nicinfo = {"kb_sent": round(Bytes_KB(nicflow.bytes_sent)/uptime,2), "kb_recv": round(Bytes_KB(nicflow.bytes_recv)/uptime,2),
                       "packets_sent": nicflow.packets_sent//uptime, "packets_recv": nicflow.packets_recv//uptime,"device":{}}
            for k, v in psutil.net_if_addrs().items():
                if v[0].address and v[0].netmask and v[0].broadcast:
                    nicinfo['device'].setdefault(k, {"name": k, "address": v[0].address, "netmask": v[0].netmask,
                                           "broadcast": v[0].broadcast})
            response.data=nicinfo

        except Exception as e:
            msg = "%s linux NicPlugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response
