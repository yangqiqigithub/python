from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator   # Django内置分页功能模块
from api import models
import json
import datetime
# Create your views here.




def show_hosts(request):
    '''
    显示搜索下拉框的默认值
    :param request:
    :return:
    '''
    if request.method=='GET':
        #平台
        platform_set=set()
        for name in models.platform.objects.all():
            platform_set.add(name.platname)
        #账号
        account_set=set()
        for account in models.account.objects.all():
            account_set.add(account.username)
        #项目
        item_set=set()
        for item in models.item.objects.all():
            item_set.add(item.itemname)
        #区域
        area_set=set()
        for area in models.area.objects.all():
            area_set.add(area.property_area)
        data={
            "platform":platform_set,
            "account":account_set,
            "item":item_set,
            "area":area_set
        }

    return render(request, 'show_hosts.html', {'data':data})



def get_hosts_json(request):
    '''
    从数据库里获取主机列表展示
    layui需要的格式为 {"code":0,"msg":"","count":1000,"data":[{"hostname":"","pri_ip":""},{},]}
    :param request:
    :return:  返回的必须是json格式的数据
    '''

    if request.method=='GET':

        searchinfo={}
        hostname=request.GET.get('hostname').strip()
        pri_ip=request.GET.get('pri_ip').strip()
        pub_ip=request.GET.get('pub_ip').strip()
        status=request.GET.get('status').strip()
        platform=request.GET.get('platform').strip()
        account=request.GET.get('account').strip()
        item=request.GET.get('item').strip()
        area=request.GET.get('area').strip()


        if pri_ip:
            searchinfo.setdefault('pri_ip',pri_ip)
        if pub_ip:
            searchinfo.setdefault('pub_ip',pub_ip)
        if status:
            searchinfo.setdefault('status',status)
        if platform:
            platform_id=models.platform.objects.filter(platname=platform).first().id
            searchinfo.setdefault('platform_id',platform_id)
        if account:
            account_id=models.account.objects.filter(username=account).first().id
            searchinfo.setdefault('account_id',account_id)
        if item:
            item_id=models.item.objects.filter(itemname=item).first().id
            searchinfo.setdefault('item_id',item_id)

        projectid_list = []
        if area:
            for i in models.area.objects.filter(property_area=area):
                projectid_list.append(i.project_id)


        #hostname是模糊查询所以得单独拿出来，不能放在字典里
        #区域，一个中文区域有几个账号就对应记得project_id，也比较特殊得单独拿出来
        if projectid_list and searchinfo and hostname:
            db_list=models.hosts.objects.filter(area_id__in=projectid_list,hostname__contains=hostname,**searchinfo)

        if projectid_list and searchinfo and not  hostname:
            db_list = models.hosts.objects.filter(area_id__in=projectid_list, **searchinfo)


        if projectid_list and not searchinfo and not hostname:
            db_list=models.hosts.objects.filter(area_id__in=projectid_list)

        if projectid_list and not searchinfo and hostname:
            db_list=models.hosts.objects.filter(area_id__in=projectid_list,hostname__contains=hostname)


        if searchinfo and not projectid_list and not hostname:
            db_list=models.hosts.objects.filter(**searchinfo)

        if searchinfo and not projectid_list and  hostname:
            db_list=models.hosts.objects.filter(hostname__contains=hostname,**searchinfo)

        if hostname and not projectid_list and not searchinfo:
            db_list = models.hosts.objects.filter(hostname__contains=hostname)


        #空搜索和页面刚打开的时候显示这个，按照页数显示所有主机
        if not projectid_list and not searchinfo and not hostname:
            db_list=models.hosts.objects.all()

        host_list=[]
        for host in db_list:
            config=str(host.cpu)+'核'+str(host.memory)+'G'
            dic={"id":host.id,"host_id":host.host_id,"hostname": host.hostname, "pri_ip": host.pri_ip, "pub_ip": host.pub_ip,
                 "status": host.status,"image": host.image_name, "config":config,"platform": host.platform.platname,
                 "account": host.account.username,"item":host.item.itemname, "region": host.area.property_area,"ctime":host.ctime,}
            host_list.append(dic)
        #
        pageIndex = request.GET.get('page')  # 前台传的值，当前页面处于第几页
        pageSize = request.GET.get('limit')  # 前台传的值，每页展示多少条数据
        pageInator = Paginator(host_list, pageSize)  # 导入分页模块分页操作，不写前端只展示一页数据<django.core.paginator.Paginator object at 0x10d25e250>
        contacts = pageInator.page(pageIndex)  # 导入分页模块分页操作，不写前端只展示一页数据，<Page 1 of 1>  当前页 of 总页数
        '''
        pageIndex 1
        pageSize 20
        pageInator <django.core.paginator.Paginator object at 0x10d25e250>
        contacts <Page 1 of 1>
        '''
        '''
        res=[]
        for i in contacts:
            res.append(i)
        print(res)
        Result = {"code": 0, "msg": "",  "count":dataCount, "data": res}
        # json.dumps(Result, cls=DateEncoder)没有时间字段问题可直接返回此代码。有就返回下面代码
        return HttpResponse(json.dumps(Result, cls=DateEncoder), content_type="application/json")
        '''
        res = []
        for i in contacts:
            res.append(i)
        result = {"code":0,"msg":"", "count":len(host_list), "data":res}
        return HttpResponse(json.dumps(result, cls=DateEncoder), content_type="application/json")


# 解决时间字段json问题
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

def hostToitem(request):
    '''
    将主机加入项目
    :param request:
    :return:
    '''
    if request.method=='POST':
        print(request.POST)
        itemname=request.POST.get('item')
        hostid_list=request.POST.getlist('hostid_list')
        item_id=models.item.objects.filter(itemname=itemname).first().id
        s=models.hosts.objects.filter(id__in=hostid_list).update(item_id=item_id)
        if s==0:
            msg='加入失败'
        else:
            msg='加入成功!'

    return  HttpResponse(msg)


def hostinfo(request,id):
    '''
    展示某台主机的详细信息
    :param request:
    :return:
    '''
    obj=models.hosts.objects.filter(id=id).first()
    return render(request,'hostinfo.html',{'obj':obj})




def show_dbs(request):

    if request.method=='GET':
        #项目
        item_set=set()
        for item in models.item.objects.all():
            item_set.add(item.itemname)
        data={
            "item":item_set,
        }
        return render(request,'show_dbs.html',{'data':data})

def get_dbs_json(request):
    if request.method=='GET':
        type=request.GET.get('type','')
        dbname=request.GET.get('dbname','')
        if type and dbname:
            db_list=models.dbs.objects.filter(dbname__contains=dbname,type=type)
        if type and not dbname:
            db_list = models.dbs.objects.filter(type=type)
        if dbname and  not type:
            db_list = models.dbs.objects.filter(dbname__contains=dbname)
        if not dbname and not type:
            db_list = models.dbs.objects.all()


        show_db_list=[]
        for db in db_list:
            config=str(db.cpu)+'核'+str(db.memory)+'G'+str(db.disk)+'G'
            dic={"id":db.id,"db_id":db.db_id,"dbname": db.dbname,"type":db.type,"mode":db.mode,"pri_ip": db.pri_ip, "pub_ip": db.pub_ip,
                 "status": db.status,"version": db.version, "config":config,"platform": db.platform.platname,
                 "account": db.account.username,"item":db.item.itemname, "region": db.area.property_area,"ctime":db.ctime,}
            show_db_list.append(dic)
        #
        pageIndex = request.GET.get('page')  # 前台传的值，当前页面处于第几页
        pageSize = request.GET.get('limit')  # 前台传的值，每页展示多少条数据
        pageInator = Paginator(show_db_list, pageSize)  # 导入分页模块分页操作，不写前端只展示一页数据<django.core.paginator.Paginator object at 0x10d25e250>
        contacts = pageInator.page(pageIndex)  # 导入分页模块分页操作，不写前端只展示一页数据，<Page 1 of 1>  当前页 of 总页数

        res = []
        for i in contacts:
            res.append(i)
        result = {"code":0,"msg":"", "count":len(show_db_list), "data":res}
        return HttpResponse(json.dumps(result, cls=DateEncoder), content_type="application/json")

def dbToitem(request):
    '''
    将数据库加入项目
    :param request:
    :return:
    '''
    if request.method=='POST':
        itemname=request.POST.get('item')
        dbid_list=request.POST.getlist('dbid_list')
        item_id=models.item.objects.filter(itemname=itemname).first().id
        s=models.dbs.objects.filter(id__in=dbid_list).update(item_id=item_id)
        if s==0:
            msg='加入失败'
        else:
            msg='加入成功!'

    return  HttpResponse(msg)