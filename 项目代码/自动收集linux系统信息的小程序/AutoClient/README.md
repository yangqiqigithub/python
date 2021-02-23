# 程序功能
自动收集linux系统基本的系统和硬件配置信息，以及硬件使用情况
# 使用方法
### 模块安装
pip3 install requests
pip3 install psutil

### 运行方式
python3 ./bin/auto-client.py

### 运行结果
```
{
    "version": "CentOS Linux release 7.5.1804 (Core)", 
    "hostname": "m", 
    "cpu": {
        "status": true, 
        "message": null, 
        "data": {
            "cpu_physical_count": 1, 
            "cpu_core_count": 2, 
            "cpu_load_tuple": [
                0, 
                0.02, 
                0.05
            ], 
            "cpu_total_util": 0
        }, 
        "error": null
    }, 
    "disk": {
        "status": true, 
        "message": null, 
        "data": {
            "/dev/vda1": {
                "device": "/dev/vda1", 
                "mountpoint": "/", 
                "fstype": "ext4", 
                "total_GB": 39, 
                "used_GB": 22, 
                "percent": 60, 
                "r/s": 46, 
                "w/s": 268, 
                "rKB/s": 1700, 
                "wKB/s": 4170
            }
        }, 
        "error": null
    }, 
    "memory": {
        "status": true, 
        "message": null, 
        "data": {
            "total": 3, 
            "used": 0, 
            "percent": 32.6
        }, 
        "error": null
    }, 
    "nic": {
        "status": true, 
        "message": null, 
        "data": {
            "kb_sent": 58.28, 
            "kb_recv": 58.5, 
            "packets_sent": 59, 
            "packets_recv": 59, 
            "device": {
                "eth0": {
                    "name": "eth0", 
                    "address": "192.168.0.13", 
                    "netmask": "255.255.255.0", 
                    "broadcast": "192.168.0.255"
                }
            }
        }, 
        "error": null
    }, 
    "swap": {
        "status": true, 
        "message": null, 
        "data": {
            "total": 0, 
            "used": 0, 
            "percent": 0
        }, 
        "error": null
    }, 
    "unique_id": "1614073456qdgs"
}

```