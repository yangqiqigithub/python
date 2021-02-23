#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.plugins.basic import BasicPlugin
from config import settings
import importlib


def get_server_info():
    """
    获取服务器基本信息
    """
    response = BasicPlugin().linux()
    if not response.status:
        return response
    for k, v in settings.PLUGINS_DICT.items():
        module_path, cls_name = v.rsplit('.', 1)
        cls = getattr(importlib.import_module(module_path), cls_name)
        obj = cls().linux()
        response.data[k] = obj
    return response


