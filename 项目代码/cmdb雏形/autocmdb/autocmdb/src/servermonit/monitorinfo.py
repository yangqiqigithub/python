from autocmdb.settings import MONITOR_DICT
from lib.serialize import Json
from src.servermonit.basic import BasicPlugin
import importlib


def get_monitor_info(host_dict):
    response = BasicPlugin(host_dict).linux()

    for k, v in MONITOR_DICT.items():
        module_path, cls_name = v.rsplit('.', 1)
        cls = getattr(importlib.import_module(module_path), cls_name)
        obj = cls(host_dict).linux()
        response.data[k] = obj
    monitor_json = Json.dumps(response.data)
    return monitor_json
