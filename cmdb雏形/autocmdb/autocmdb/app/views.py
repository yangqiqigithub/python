from django.shortcuts import render,HttpResponse,redirect
from src.serverinfo.serverinfo import get_server_info
from src.servermonit.monitorinfo import get_monitor_info
from lib.common import savefile
from lib.common import  timestamp_strftime
from lib.common import strftime_timestamp
from concurrent.futures import ThreadPoolExecutor
from app import models
import json
from lib.response import BaseResponse
from lib.log import Logger
import traceback
import  time
import re

def login(request):

    if request.method=='GET':
        return render(request,'login.html')

    if request.method=='POST':
        return redirect('/index/')

def signup(request):

    if request.method=='GET':
        return render(request,'signup.html')

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

def forgot_password(request):

    if request.method=='GET':
        return render(request,'forgot-password.html')

def reset_password(request):
    if request.method=='GET':
        return render(request,'reset-password.html')

def hosts(request):
    if request.method=='GET':
        hosts_set_dict=models.HostsInfo.objects.values('id','hostname','ip','os_version','cpu','memory','unique_id')
        hosts_list=[]

        for host_dict in hosts_set_dict:
            hostname=host_dict['hostname']
            ip=host_dict['ip']
            out_ip=models.HostConn.objects.filter(unique_id=host_dict['unique_id']).values('ip').first()['ip']
            os_version=host_dict['os_version']
            cpu_cores=eval(host_dict['cpu'])['cpu_count']
            mem_total=eval(host_dict['memory'])['MemTotal']
            id=host_dict['id']

            dic={"hostname":hostname,
                    "ip":ip,
                    "out_ip":out_ip,
                    "os_version":os_version,
                    "cpu_cores":cpu_cores,
                    "mem_total":mem_total,
                    "id":id}
            hosts_list.append(dic)

        return render(request, 'hosts.html',{'hosts_list':hosts_list})

def users(request):
    if request.method=='GET':
        return render(request, 'users.html')

def  roles(request):
    if request.method=='GET':
        return render(request,'roles.html')

def items(request):
    if request.method=='GET':
        return  render(request,'items.html')

def add_roles(request):

    if request.method=='GET':
        return render(request,'add_roles.html')

def add_users(request):
    if request.method=='GET':
        return render(request,'add_users.html')

def host_detail(request,id):
    if request.method=='GET':
        obj = models.HostsInfo.objects.filter(id=id).first()
        inip=eval(obj.nic)['eth0']['ipaddrs']+'/'+eval(obj.nic)['eth0']['netmask']
        outip=models.HostConn.objects.filter(unique_id=obj.unique_id).values('ip').first()['ip']
        os_version=obj.os_version

        memory = {"total":eval(obj.memory)['MemTotal'],
                  "free":eval(obj.memory)['MemFree'],
                  "aval":eval(obj.memory)['MemAvailable']}

        cpu = {"cpu_cores":eval(obj.cpu)['cpu_count'],
               "cpu_count":eval(obj.cpu)['cpu_physical_count'],
               "cpu_model":eval(obj.cpu)['cpu_model']}

        main_board = {"manufacturer":eval(obj.main_board)['manufacturer'],
                      "model":eval(obj.main_board)['model'],
                      "sn":eval(obj.main_board)['sn']}


        nic={"status":eval(obj.nic)['eth0']['up'],
             "inip":inip,
             "hwaddr":eval(obj.nic)['eth0']['hwaddr']}


        disk_list=[]
        for i in eval(obj.disk).values():
            disk_list.append(i)
        print(disk_list)

        detail_dict={
            "inip":inip,
            "outip":outip,
            "os_version": os_version,
            "main_board": main_board,
            "cpu": cpu,
            "memory": memory,
            "nic":nic,
            "disk_count":len(disk_list)+1
        }

        return render(request, 'host_detail.html',{'detail_dict':detail_dict,'disk_list':disk_list})

def mysql_detail(request):
    if request.method=='GET':
        return render(request, 'mysql_detail.html')

def mysql_count(request):
    if request.method=='GET':
        return render(request,'mysql_count.html')

def add_host(request):
    if request.method=='GET':
        return render(request,'add_host.html')

    if request.method=='POST':
        host_dict=request.POST

        db_unique_id_set = set()
        for i in models.HostsInfo.objects.values('unique_id'):
            db_unique_id_set.add(i['unique_id'])

        serverinfo_dict=json.loads(get_server_info(host_dict))
        try:
            ip = serverinfo_dict['nic']['data']['eth0']['ipaddrs']
        except Exception as e:
            ip = '0.0.0.0'
        create_data_dict = {
            "os_version": serverinfo_dict['os_version'],
            "ip": ip,
            "hostname": serverinfo_dict['hostname'],
            "unique_id": serverinfo_dict['unique_id'],
            "cpu": serverinfo_dict['cpu']['data'],
            "disk": serverinfo_dict['disk']['data'],
            "main_board": serverinfo_dict['main_board']['data'],
            "memory": serverinfo_dict['memory']['data'],
            "nic": serverinfo_dict['nic']['data'],
        }

        if serverinfo_dict['unique_id'] in db_unique_id_set:
            models.HostsInfo.objects.filter(unique_id=serverinfo_dict['unique_id']).update(**create_data_dict)
            print('%s-%s已经存在，现在被更新' %(serverinfo_dict['unique_id'],ip))
        else:
            models.HostsInfo.objects.create(**create_data_dict)
            print('%s-%s被插入' %(serverinfo_dict['unique_id'],ip))

        # 添加主机 默认会记录主机的登录信息，为了一定定时更新任务使用
        db_conn_set = set()
        for c in models.HostConn.objects.values('unique_id'):
            db_conn_set.add(c['unique_id'])

        create_conn_dict = {
            'ip':host_dict['ip'],
            'port':host_dict['port'],
            'username':host_dict['username'],
            'password':host_dict['password']
        }
        create_conn_dict.setdefault('unique_id', serverinfo_dict['unique_id'])

        if create_conn_dict['unique_id'] in db_conn_set:
            models.HostConn.objects.filter(unique_id=create_conn_dict['unique_id']).update(**create_conn_dict)
        else:
            models.HostConn.objects.create(**create_conn_dict)

        return  redirect('/hosts/')

def add_morehosts(request):
    if request.method=='GET':
        return render(request,'add_morehosts.html')

    if request.method=='POST':
        file=savefile(request.FILES.get('filename'))
        with open(file,'r',encoding='utf8') as f:
            hosts_conn_list=eval(f.read())

        db_unique_id_set = set() #获取数据库里存储的unique_id集合
        for i in models.HostsInfo.objects.values('unique_id'):
            db_unique_id_set.add(i['unique_id'])

        p = ThreadPoolExecutor()
        objs = []

        for host_dict in hosts_conn_list:
            obj = p.submit(get_server_info,host_dict)
            objs.append(obj)
        p.shutdown()

        server_unique_id_set=set()  #获取新采集的数据的unique_id集合
        for obj in objs:
            serverinfo_dict = json.loads(obj.result())
            server_unique_id_set.add(serverinfo_dict['unique_id'])

        diff=server_unique_id_set.difference(db_unique_id_set) #拿到两个集合的差集,差集的数据应该插入
        same=server_unique_id_set.intersection(db_unique_id_set)# 拿到两个集合的交集,交集的数据应该被更新

        for obj in objs:
            serverinfo_dict = json.loads(obj.result())
            try:
                ip = serverinfo_dict['nic']['data']['eth0']['ipaddrs']
            except Exception as e:
                ip = '0.0.0.0'
            create_data_dict = {
                "os_version": serverinfo_dict['os_version'],
                "ip": ip,
                "hostname": serverinfo_dict['hostname'],
                "unique_id": serverinfo_dict['unique_id'],
                "cpu": serverinfo_dict['cpu']['data'],
                "disk": serverinfo_dict['disk']['data'],
                "main_board": serverinfo_dict['main_board']['data'],
                "memory": serverinfo_dict['memory']['data'],
                "nic": serverinfo_dict['nic']['data'],
            }

            if diff: #差集的逻辑
                if serverinfo_dict['unique_id'] in diff:
                    models.HostsInfo.objects.create(**create_data_dict)
                    print('%s-%s被插入' % (serverinfo_dict['unique_id'], ip))
            if same:
                if serverinfo_dict['unique_id'] in same:
                    models.HostsInfo.objects.filter(unique_id=serverinfo_dict['unique_id']).update(**create_data_dict)
                    print('%s-%s已经存在，现在被更新' % (serverinfo_dict['unique_id'], ip))

            #添加主机 默认会记录主机的登录信息，为了一定定时更新任务使用
            db_conn_set=set()
            for c in models.HostConn.objects.values('unique_id'):
                db_conn_set.add(c['unique_id'])

            create_conn_dict=serverinfo_dict['conninfo']
            create_conn_dict.setdefault('unique_id',serverinfo_dict['unique_id'])

            if create_conn_dict['unique_id'] in db_conn_set:
                models.HostConn.objects.filter(unique_id=create_conn_dict['unique_id']).update(**create_conn_dict)
            else:
                models.HostConn.objects.create(**create_conn_dict)

        return redirect('/hosts/')

def flush_serverinfo(request):
    hosts_conn_list=models.HostConn.objects.values('ip', 'port', 'username', 'password')
    p = ThreadPoolExecutor()
    objs = []
    for host_dict in hosts_conn_list:
        obj = p.submit(get_server_info, host_dict)
        objs.append(obj)
    p.shutdown()
    for obj in objs:
        serverinfo_dict = json.loads(obj.result())
        try:
            ip = serverinfo_dict['nic']['data']['eth0']['ipaddrs']
        except Exception as e:
            ip = '0.0.0.0'
        create_data_dict = {
            "os_version": serverinfo_dict['os_version'],
            "ip": ip,
            "hostname": serverinfo_dict['hostname'],
            "unique_id": serverinfo_dict['unique_id'],
            "cpu": serverinfo_dict['cpu']['data'],
            "disk": serverinfo_dict['disk']['data'],
            "main_board": serverinfo_dict['main_board']['data'],
            "memory": serverinfo_dict['memory']['data'],
            "nic": serverinfo_dict['nic']['data'],
        }
        models.HostsInfo.objects.filter(unique_id=serverinfo_dict['unique_id']).update(**create_data_dict)
        print('%s-%s被更新' % (serverinfo_dict['unique_id'], ip))

    return redirect('/hosts/')

def flush_minitorinfo(request):
    hosts_conn_list = models.HostConn.objects.values('ip', 'port', 'username', 'password','unique_id')
    ctime=int(time.time())
    # print(hosts_conn_list)
    p = ThreadPoolExecutor()
    objs = []
    for host_dict in hosts_conn_list:
        id=models.HostsInfo.objects.filter(unique_id=host_dict['unique_id']).first().id
        conn_dict={'ip':host_dict['ip'], 'port':host_dict['port'], 'username':host_dict['username'], 'password':host_dict['password']}
        obj = p.submit(get_monitor_info, conn_dict)
        dic =json.loads(obj.result())
        dic.setdefault('id',id)
        objs.append(dic)
    p.shutdown()
    for data_dict in objs:
        # 服务器基本监控数据入库操作
        response = BaseResponse()
        try:
            models.HostTasks.objects.create(
                total=data_dict['cmst']['data']['tasks']['total'],
                running=data_dict['cmst']['data']['tasks']['running'],
                sleeping=data_dict['cmst']['data']['tasks']['sleeping'],
                stopped=data_dict['cmst']['data']['tasks']['stopped'],
                zombie=data_dict['cmst']['data']['tasks']['zombie'],
                host_id=data_dict['id'],
                ctime=ctime

            )

            models.HostLoadavg.objects.create(
                one=data_dict['cmst']['data']['loadavg'][0],
                five=data_dict['cmst']['data']['loadavg'][1],
                fifteen=data_dict['cmst']['data']['loadavg'][2],
                host_id=data_dict['id'],
                ctime=ctime
            )

            models.HostCpu.objects.create(
                util=data_dict['cmst']['data']['cpu']['util'],
                host_id=data_dict['id'],
                ctime=ctime
            )

            models.HostMem.objects.create(
                total=data_dict['cmst']['data']['mem']['total'],
                used=data_dict['cmst']['data']['mem']['used'],
                buffcache=data_dict['cmst']['data']['mem']['buff/cache'],
                util=data_dict['cmst']['data']['mem']['util'],
                host_id=data_dict['id'],
                ctime=ctime
            )

            models.HostSwap.objects.create(
                total=data_dict['cmst']['data']['swap']['total'],
                util=data_dict['cmst']['data']['swap']['util'],
                used=data_dict['cmst']['data']['swap']['free'],
                avail=data_dict['cmst']['data']['swap']['avail'],
                host_id=data_dict['id'],
                ctime=ctime
            )

            models.HostNic.objects.create(
                iface=data_dict['nic']['data']['iface'],
                rxpcks=data_dict['nic']['data']['rxpck/s'],
                txpcks=data_dict['nic']['data']['txpck/s'],
                rxkbs=data_dict['nic']['data']['rxkb/s'],
                txkbs=data_dict['nic']['data']['txkb/s'],
                rxcmps=data_dict['nic']['data']['rxcmp/s'],
                txcmps=data_dict['nic']['data']['txcmp/s'],
                rxmcsts=data_dict['nic']['data']['rxmcst/s'],
                host_id=data_dict['id'],
                ctime=ctime
            )
            for v in data_dict['disk']['data'].values():
                models.HostDisk.objects.create(
                    device=v['device'],
                    rs=v['r/s'],
                    ws=v['w/s'],
                    rkBs=v['rkB/s'],
                    wkBs=v['wkB/s'],
                    io_util=v['io_util'],
                    total=v['total'],
                    used=v['used'],
                    size_util=v['size_util'],
                    host_id=data_dict['id'],
                    ctime=ctime
                )


        except  Exception as e:

            msg = "%s-%s 监控数据入库错误  Error:%s"
            Logger().log(msg % (data_dict['hostname'], data_dict['ip'], traceback.format_exc()), False)
            response.status = False
            response.error = msg % (data_dict['hostname'], data_dict['ip'], traceback.format_exc())
    return HttpResponse('GET MONITOR DATA SUCCESSFUL!!')



def host_monitor(request,id):
    hid=id
    device_set=set()
    for h in models.HostDisk.objects.filter(host_id=hid):
        device_set.add(h.device)
    return render(request,'host_monitor.html',{'hid':id,'device_set':device_set})

def get_monitor_data(request):


    if request.method=='GET':
        return HttpResponse('哪里来的get请求，可恶！')

    if request.method=='POST':
        monitor_data={}

        time_range=request.POST.get('time_range')  # 2019-09-19 00:00:00 - 2019-10-24 00:00:00
        hid=request.POST.get('hid')

        #页面加载和自动刷新
        if time_range == '0':
            time_stop = int(time.time())
            time_start = int(time_stop - 3600)
            print('开始时间:',time_start,timestamp_strftime(time_start))
            print('结束时间:',time_stop,timestamp_strftime(time_stop))

        #6小时前的数据
        elif time_range == '6':
            time_stop = int(time.time())
            time_start = int(time_stop - 21600)
            print('开始时间:', time_start, timestamp_strftime(time_start))
            print('结束时间:', time_stop, timestamp_strftime(time_stop))

        #12小时前的数据
        elif time_range == '12':
            time_stop = int(time.time())
            time_start = int(time_stop - 43200)
            print('开始时间:', time_start, timestamp_strftime(time_start))
            print('结束时间:', time_stop, timestamp_strftime(time_stop))

        #一天前的数据
        elif time_range == '1':
            time_stop = int(time.time())
            time_start = int(time_stop - 86400)
            print('开始时间:', time_start, timestamp_strftime(time_start))
            print('结束时间:', time_stop, timestamp_strftime(time_stop))

        #3天前的数据
        elif time_range == '3':
            time_stop = int(time.time())
            time_start = int(time_stop - 259200)
            print('开始时间:', time_start, timestamp_strftime(time_start))
            print('结束时间:', time_stop, timestamp_strftime(time_stop))

        #7天前的数据
        elif time_range == '7':
            time_stop = int(time.time())
            time_start = int(time_stop - 604800)
            print('开始时间:', time_start, timestamp_strftime(time_start))
            print('结束时间:', time_stop, timestamp_strftime(time_stop))

        #14天前的数据
        elif time_range == '14':
            time_stop = int(time.time())
            time_start = int(time_stop - 1209600)
            print('开始时间:', time_start, timestamp_strftime(time_start))
            print('结束时间:', time_stop, timestamp_strftime(time_stop))

        else:
            time_re_list = re.findall('\d+-\d+-\d+\s\d+:\d+:\d+', time_range)
            print(time_re_list)
            time_start = strftime_timestamp(time_re_list[0])
            time_stop = strftime_timestamp(time_re_list[1])

            print('开始时间:',time_start,time_re_list[0])
            print('结束时间:',time_stop,time_re_list[1])


        #采集cpu利用率展示数据
        cpu_data_list = []
        cpu_time_list = []
        for h in models.HostCpu.objects.filter(host_id=hid, ctime__range=[time_start, time_stop]):
            cpu_data_list.append(h.util)
            cpu_time_list.append(timestamp_strftime(h.ctime))

        #采集内存利用率展示数据
        mem_data_list = []
        mem_time_list = []
        for h in models.HostMem.objects.filter(host_id=hid, ctime__range=[time_start, time_stop]):
            mem_data_list.append(h.util)
            mem_time_list.append(timestamp_strftime(h.ctime))

        #采集系统负载展示数据
        load5_data_list = []
        load10_data_list = []
        load15_data_list = []
        load_time_list = []
        for h in models.HostLoadavg.objects.filter(host_id=hid, ctime__range=[time_start, time_stop]):
            load5_data_list.append(h.one)
            load10_data_list.append(h.five)
            load15_data_list.append(h.fifteen)
            load_time_list.append(timestamp_strftime(h.ctime))


        #采集交换分区利用率展示
        swap_data_list = []
        swap_time_list = []
        for h in models.HostSwap.objects.filter(host_id=hid, ctime__range=[time_start, time_stop]):
            swap_data_list.append(h.util)
            swap_time_list.append(timestamp_strftime(h.ctime))



        #采集进程数量展示
        task_running_list = []
        task_sleeping_list = []
        task_stopped_list = []
        task_zombile_list = []
        task_time_list = []
        for h in models.HostTasks.objects.filter(host_id=hid, ctime__range=[time_start, time_stop]):
            task_running_list.append(h.running)
            task_sleeping_list.append(h.sleeping)
            task_stopped_list.append(h.stopped)
            task_zombile_list.append(h.zombie)
            task_time_list.append(timestamp_strftime(h.ctime))


        #采集网卡监控数据
        disk_rxpcks_list = []
        disk_txpcks_list = []
        disk_rxcmps_list = []
        disk_txcmps_list = []
        disk_rxmcsts_list = []
        disk_rxkbs_list = []
        disk_txkbs_list = []
        nic_time_list = []
        nic_name=''
        for h in models.HostNic.objects.filter(host_id=hid, ctime__range=[time_start, time_stop]):
            nic_name=h.iface
            disk_rxpcks_list.append(h.rxpcks)
            disk_txpcks_list.append(h.txpcks)
            disk_rxcmps_list.append(h.rxcmps)
            disk_txcmps_list.append(h.txcmps)
            disk_rxmcsts_list.append(h.rxmcsts)
            disk_rxkbs_list.append(h.rxkbs)
            disk_txkbs_list.append(h.txkbs)
            nic_time_list.append(timestamp_strftime(h.ctime))



        #采集磁盘数据展示
        disk_io_data_list = []
        disk_size_data_list = []
        disk_rs_data_list=[]
        disk_ws_data_list=[]
        disk_rkBs_data_list=[]
        disk_wkBs_data_list=[]
        disk_time_list = []
        device_list=[]


        for h in models.HostDisk.objects.filter(host_id=hid):
            device_list.append(h.device)
        device_list=list(set(device_list))

        device='vda'
        for i in device_list:
            if i=='vda':
                device='vda'
            else:
                device=device_list[0]

        for h in models.HostDisk.objects.filter(host_id=hid, ctime__range=[time_start, time_stop]):
            if h.device==device:
                disk_size_data_list.append(h.size_util)
                disk_io_data_list.append(h.io_util)
                disk_rs_data_list.append(h.rs)
                disk_ws_data_list.append(h.ws)
                disk_rkBs_data_list.append(h.rkBs)
                disk_wkBs_data_list.append(h.wkBs)
                disk_time_list.append(timestamp_strftime(h.ctime))









        #最终传输给前端的数据
        monitor_data = {
            "cpu": {
                "cpu_util": cpu_data_list,
                "time_range": cpu_time_list,
            },
            "mem": {
                "mem_util": mem_data_list,
                "time_range": mem_time_list,
            },
            "swap": {
                "swap_util": swap_data_list,
                "time_range": swap_time_list,
            },
            "loadavg":{
                "m5":load5_data_list,
                "m10": load10_data_list,
                "m15": load15_data_list,
                "time_range": load_time_list,

            },
            "tasks":{
                "running": task_running_list,
                "sleeping": task_sleeping_list,
                "stopped": task_stopped_list,
                "zombile": task_zombile_list,
                "time_range": task_time_list,

            },
            "nic":{
                "nic_name": nic_name,
                "disk_rxpcks_list": disk_rxpcks_list,
                "disk_txpcks_list": disk_txpcks_list,
                "disk_rxcmps_list": disk_rxcmps_list,
                "disk_txcmps_list": disk_txcmps_list,
                "disk_rxmcsts_list": disk_rxmcsts_list,
                "disk_rxkbs_list": disk_rxkbs_list,
                "disk_txkbs_list": disk_txkbs_list,
                "time_range": nic_time_list,

            },
            "disk": {
                "device":device,
                "disk_io_data_list": disk_io_data_list,
                "disk_size_data_list":disk_size_data_list,
                "disk_rs_data_list": disk_rs_data_list,
                "disk_ws_data_list": disk_ws_data_list,
                "disk_rkBs_data_list": disk_rkBs_data_list,
                "disk_wkBs_data_list": disk_wkBs_data_list,
                "time_range": disk_time_list,

            }
        }


        data=json.dumps(monitor_data)


        if request.POST.get('device'):
            print('我是前端来的device',request.POST.get('device'))

        return HttpResponse(data)



