#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import os
from lib.serialize import Json
from lib.log import Logger
from config import settings

from lib.common import unique_code

class AutoBase(object):
    def __init__(self):
        self.asset_api = settings.ASSET_API

    def post_asset(self, msg):
        """
        post方式向接口提交资产信息
        :param msg:
        :param callback:
        :return:
        """
        status = True
        try:
            response = requests.post(
                url=self.asset_api,
                json=msg
            )
        except Exception as e:
            response = e
            status = False




class AutoAgent(AutoBase):
    def __init__(self):
        self.cert_file_path = settings.CERT_FILE_PATH
        super(AutoAgent, self).__init__()

    def load_local_cert(self):
        """
        获取本地以为标识
        :return:
        """
        if not os.path.exists(self.cert_file_path):
            return None
        with open(self.cert_file_path, mode='r') as f:
            data = f.read()
        if not data:
            return None
        cert = data.strip()
        return cert

    def write_local_cert(self):
        """
        写入本地以为标识
        :param cert:
        :return:
        """
        with open(settings.CERT_FILE_PATH, mode='w') as f:
            cert=unique_code()
            f.write(cert)
    def process(self,info):
        """

        :return:
        """
        server_info = info
        if not server_info.status:
            return
        local_cert = self.load_local_cert()
        if local_cert:
            pass
        else:
            self.write_local_cert()
            local_cert = self.load_local_cert()
        server_info.data.setdefault('unique_id',local_cert)
        server_json = Json.dumps(server_info.data)
        print(server_json)
        self.post_asset(server_json)
