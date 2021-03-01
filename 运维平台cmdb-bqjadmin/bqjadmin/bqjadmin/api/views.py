from django.shortcuts import render,HttpResponse,redirect
from api import models
# Create your views here.

def asset(request):
    import json
    if request.method == 'POST':
        server_info = json.loads(request.body.decode('utf8'))
        server_info={'type': '0', 'all_host_list': [{'host_id': '03500d12-3bbf-42ca-ab80-eaf33a0876bf', 'hostname': '区块链取证项目-取证引擎01', 'pri_ip': '192.168.0.124', 'pub_ip': '121.36.32.103', 'status': 'ACTIVE', 'image_name': 'CentOS 7.5 64bit', 'memory': 4096, 'cpu': 2, 'ctime': '2019-12-10T03:53:22Z', 'volume_list': [{'volume_size': 150, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': '4a478b34-810f-4695-a554-fe33e92067b1', 'hostname': '区块链取证项目-取证引擎02', 'pri_ip': '192.168.0.139', 'pub_ip': '119.3.208.32', 'status': 'ACTIVE', 'image_name': 'CentOS 7.5 64bit', 'memory': 4096, 'cpu': 2, 'ctime': '2019-12-10T03:53:22Z', 'volume_list': [{'volume_size': 150, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': 'cedfe4d4-0242-4a28-a2b8-f3a7b7ea4084', 'hostname': '区块链取证项目-网页取证01', 'pri_ip': '192.168.0.188', 'pub_ip': '114.116.240.160', 'status': 'ACTIVE', 'image_name': 'CentOS 7.5 64bit', 'memory': 4096, 'cpu': 2, 'ctime': '2019-12-10T03:53:22Z', 'volume_list': [{'volume_size': 150, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': '03c3c859-6135-42f5-8e49-0b0c3ca989d6', 'hostname': '区块链取证项目-网页取证02', 'pri_ip': '192.168.0.157', 'pub_ip': '119.3.167.7', 'status': 'ACTIVE', 'image_name': 'CentOS 7.5 64bit', 'memory': 4096, 'cpu': 2, 'ctime': '2019-12-10T03:53:22Z', 'volume_list': [{'volume_size': 150, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': '8224cf5b-f919-4c28-a736-bf75f32ff522', 'hostname': 'Bcos-0001', 'pri_ip': '192.168.0.78', 'pub_ip': '117.78.1.164', 'status': 'ACTIVE', 'image_name': 'CentOS 7.2 64bit', 'memory': 8192, 'cpu': 4, 'ctime': '2019-11-22T02:38:30Z', 'volume_list': [{'volume_size': 500, 'volume_device': '/dev/vdb'}, {'volume_size': 100, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': 'a104140e-d2b5-477c-9e60-d07dc757a26d', 'hostname': 'Bcos-0002', 'pri_ip': '192.168.0.175', 'pub_ip': '121.36.5.182', 'status': 'ACTIVE', 'image_name': 'CentOS 7.2 64bit', 'memory': 8192, 'cpu': 4, 'ctime': '2019-11-22T02:38:30Z', 'volume_list': [{'volume_size': 500, 'volume_device': '/dev/vdb'}, {'volume_size': 100, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': 'cc3f2375-5888-4de7-804c-e3263882c051', 'hostname': 'Bcos-0003', 'pri_ip': '192.168.0.92', 'pub_ip': '139.9.117.19', 'status': 'ACTIVE', 'image_name': 'CentOS 7.2 64bit', 'memory': 8192, 'cpu': 4, 'ctime': '2019-11-22T02:38:30Z', 'volume_list': [{'volume_size': 500, 'volume_device': '/dev/vdb'}, {'volume_size': 100, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': 'b28ef819-52ad-48f9-b415-0bca9c3a3a49', 'hostname': 'Bcos-0004', 'pri_ip': '192.168.0.17', 'pub_ip': '139.9.136.193', 'status': 'ACTIVE', 'image_name': 'CentOS 7.2 64bit', 'memory': 8192, 'cpu': 4, 'ctime': '2019-11-22T02:38:30Z', 'volume_list': [{'volume_size': 100, 'volume_device': '/dev/vda'}, {'volume_size': 500, 'volume_device': '/dev/vdb'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': 'c9c9b58a-4d01-413d-8a7d-ecc26695099c', 'hostname': 'Bcos-SDK', 'pri_ip': '192.168.0.200', 'pub_ip': '114.116.255.201', 'status': 'ACTIVE', 'image_name': 'Ubuntu 16.04 server 64bit', 'memory': 8192, 'cpu': 4, 'ctime': '2019-11-22T02:35:59Z', 'volume_list': [{'volume_size': 100, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': 'ecbbb49f-be0b-410b-ad48-607404dfeb36', 'hostname': '姜喜亮-网页取证-01', 'pri_ip': '192.168.0.39', 'pub_ip': '139.9.140.192', 'status': 'ACTIVE', 'image_name': 'CentOS 7.5 64bit', 'memory': 4096, 'cpu': 2, 'ctime': '2019-11-19T03:13:28Z', 'volume_list': [{'volume_size': 100, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': '2af2a99d-4a9c-4e70-a7e6-5051387a633e', 'hostname': 'BQJ-区块链-26', 'pri_ip': '192.168.0.71', 'pub_ip': '121.36.3.44', 'status': 'ACTIVE', 'image_name': 'Ubuntu 16.04 server 64bit', 'memory': 4096, 'cpu': 2, 'ctime': '2019-11-19T02:19:07Z', 'volume_list': [{'volume_size': 200, 'volume_device': '/dev/vdb'}, {'volume_size': 100, 'volume_device': '/dev/vda'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': 'dfd500c4-1197-4e94-957c-263c8c1bd82a', 'hostname': 'BQJ-区块链-23', 'pri_ip': '192.168.0.38', 'pub_ip': '119.3.163.55', 'status': 'ACTIVE', 'image_name': 'Ubuntu 16.04 server 64bit', 'memory': 8192, 'cpu': 4, 'ctime': '2019-11-19T02:13:07Z', 'volume_list': [{'volume_size': 100, 'volume_device': '/dev/vda'}, {'volume_size': 500, 'volume_device': '/dev/vdb'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': 'fedb3fdd-f495-4101-97bf-c7832edd3b46', 'hostname': 'BQJ-区块链-24', 'pri_ip': '192.168.0.205', 'pub_ip': '139.9.143.70', 'status': 'ACTIVE', 'image_name': 'Ubuntu 16.04 server 64bit', 'memory': 8192, 'cpu': 4, 'ctime': '2019-11-19T02:13:07Z', 'volume_list': [{'volume_size': 100, 'volume_device': '/dev/vda'}, {'volume_size': 500, 'volume_device': '/dev/vdb'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}, {'host_id': '3993a676-ac18-4add-9baf-d12666b68262', 'hostname': 'BQJ-区块链-25', 'pri_ip': '192.168.0.47', 'pub_ip': '121.36.27.63', 'status': 'ACTIVE', 'image_name': 'Ubuntu 16.04 server 64bit', 'memory': 8192, 'cpu': 4, 'ctime': '2019-11-19T02:13:07Z', 'volume_list': [{'volume_size': 100, 'volume_device': '/dev/vda'}, {'volume_size': 500, 'volume_device': '/dev/vdb'}], 'project_id': '06d8e79ec7000f282f49c006d894c073', 'platform': '华为云', 'account': 'anne-quanbq'}]}

        if server_info.get('type')=='0':
            #说明采集的是主机列表
            all_host_list=server_info.get('all_host_list')
            db_host_id_list=[ "%s" %obj.host_id for obj in models.hosts.objects.all()] #数据库里所有主机id的列表

            if all_host_list:
                for host in all_host_list:
                    host_id=host.get('host_id')
                    if host_id in db_host_id_list: #说明数据库里已经有这个主机 可能需要更新
                        pass
                    else: #说明数据库里没有这个主机，直接插入
                        platform_id=models.platform.objects.filter(platname=host.get('platform')).first().id
                        account_id=models.account.objects.filter(username=host.get('account')).first().id
                        area_id=models.area.objects.filter(project_id=host.get('project_id')).first().id
                        models.hosts.objects.create(
                            host_id=host.get('host_id'),
                            hostname = host.get('hostname'),
                            pri_ip = host.get('pri_ip'),
                            pub_ip = host.get('pub_ip'),
                            status = host.get('status'),
                            image_name = host.get('image_name'),
                            memory = host.get('memory'),
                            ctime = host.get('ctime'),
                            volume_list = host.get('volume_list'),
                            area_id=area_id,
                            platform_id=platform_id,
                            account_id=account_id
                        )

            else:
                pass #没有任何信息提交 什么都不用做


    return HttpResponse('asset')






