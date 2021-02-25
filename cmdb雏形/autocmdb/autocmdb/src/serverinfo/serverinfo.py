from autocmdb.settings import PLUGINS_DICT
from lib.serialize import Json
from src.serverinfo.basic import BasicPlugin
import importlib


def get_server_info(host_dict):
    response = BasicPlugin(host_dict).linux()

    for k, v in PLUGINS_DICT.items():
        module_path, cls_name = v.rsplit('.', 1)
        cls = getattr(importlib.import_module(module_path), cls_name)
        obj = cls(host_dict).linux()
        response.data[k] = obj
    server_json = Json.dumps(response.data)
    return server_json
