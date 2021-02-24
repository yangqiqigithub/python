from django.shortcuts import render,HttpResponse,redirect
from cmdb.utils.md5 import gen_md5
from api import models
from rbac import models as rbac_models
import json
from rbac.service.init_permission import init_permission
import datetime
from django.core.paginator import Paginator   # Django内置分页功能模块
def index(request):

    return render(request, 'index.html')


def login(request):

    if request.method=='GET':
        return render(request,'login.html')

    if request.method=='POST':
        info={'status':0,'msg':''}
        user = request.POST.get('user')
        pwd = gen_md5(request.POST.get('pwd', ''))
        # 根据用户名和密码去用户表中获取用户对象
        user = models.UserInfo.objects.filter(name=user, password=pwd).first()
        if not user:
            #return render(request, 'login.html', {'msg': '用户名或密码错误'}) 使用这个前端有时候不显示错误信息不知为啥
            info['msg']='用户名或密码错误'
        else:
            info['status']=1
            request.session['user_info'] = {'id': user.id, 'name': user.name,'nickname': user.nickname}
            # 用户权限信息的初始化
            init_permission(user, request)
            #return redirect('/index/')#如果使用重定向  页面没反应 和前端的 return false; 这个有关系 所以关于页面的跳转都放在了前端
        return HttpResponse(json.dumps(info))


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.delete()

    return redirect('/login/')


def userinfo(request,uid):
    if request.method=='GET':
        obj=models.UserInfo.objects.filter(id=uid).first()
        return render(request,'userinfo.html',{'obj':obj})

    if request.method=='POST':
        userinfo=json.loads(request.POST.get('data'))
        '''
        dict
        {'id': '1', 'username': 'yangqiqi', 'sex': '0', 'phone': '15810270864', 'email': 'yangqiqi@anne.com.cn', 
       'depart': '运维部', 'remarks': '这个是杨琪琪的账户'}
        '''
        models.UserInfo.objects.filter(id=userinfo['id']).update(
            phone=userinfo['phone'],
            email=userinfo['email'],
            gender=userinfo['sex'],
        )
        return HttpResponse('ok')

def test(request):
    print(test)
    return render(request,'test.html')

def show_users(request):
    if request.method=='GET':
        return render(request,'show_users.html')

def  get_json_user(request):


    name=request.GET.get('name','')
    if name:
        db_list=models.UserInfo.objects.filter(name__contains=name)
    else:
        # 空搜索和页面刚打开的时候显示这个，按照页数显示所有主机
        db_list = models.UserInfo.objects.all()

    user_list = []
    for user in db_list:
        if user.gender == 0:
            gender = '女'
        else:
            gender = '男'
        user_dict = {
            'id': user.id,
            'name': user.name,
            'nickname': user.nickname,
            'email': user.email,
            'phone': user.phone,
            'gender': gender,
            'depart': user.depart.title,
            'ctime': user.ctime,
            'roles': ["%s" % r.title for r in user.roles.all()],
            'operation': ''

        }
        user_list.append(user_dict)
    # #
    #
    pageIndex = request.GET.get('page')  # 前台传的值，当前页面处于第几页
    pageSize = request.GET.get('limit')  # 前台传的值，每页展示多少条数据
    pageInator = Paginator(user_list,
                           pageSize)  # 导入分页模块分页操作，不写前端只展示一页数据<django.core.paginator.Paginator object at 0x10d25e250>
    contacts = pageInator.page(pageIndex)  # 导入分页模块分页操作，不写前端只展示一页数据，<Page 1 of 1>  当前页 of 总页数
    res = []
    for i in contacts:
        res.append(i)
    result = {"code": 0, "msg": "", "count": len(user_list), "data": res}
    return HttpResponse(json.dumps(result, cls=DateEncoder), content_type="application/json")


#解决时间字段json问题
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def user_edit(request,userid):
    if request.method=='GET':
        user=models.UserInfo.objects.filter(id=userid).first()
        user_dict={
            'id':user.id,
            'name':user.name,
            'nickname':user.nickname,
            'email':user.email,
            'phone':user.phone,
            'gender':user.gender,
            'depart':user.depart.title,
            'roles':[ "%s" %r.title for r in user.roles.all() ]
        }
        departs=models.Department.objects.all()
        roles=rbac_models.Role.objects.all()
        return render(request,'user_edit.html',{'data':user_dict,'departs':departs,'roles':roles})

    if request.method=='POST':
        #单独传输一次角色列表
        user_dict=json.loads(request.POST.get('data'))
        role_list=request.POST.getlist('role_list')
        '''
        {'id': '1', 'username': 'yangqiqi', 'nickname': 'yangqiqi', 'sex': '0', 'phone': '15810270869',
         'email': 'yangqiqi@anne.com.cn', 'depart': '运维部', 'role': '测试用户', 'pass': '123456',
          'repass': '123456'}
            ['超级用户', '测试用户']
        '''
        try:
            obj = models.UserInfo.objects.filter(id=user_dict['id']).first()
            models.UserInfo.objects.filter(id=user_dict['id']).update(
                name=user_dict['username'],
                nickname=user_dict['nickname'],
                phone=user_dict['phone'],
                gender=user_dict['sex'],
                email=user_dict['email'],
                password=gen_md5(user_dict['pass']),
                depart_id=models.Department.objects.filter(title=user_dict['depart']).first().id
            )
            roleid_list = []
            for role in role_list:
                roleid_list.append(rbac_models.Role.objects.filter(title=role).first().id)

            obj.roles.set(roleid_list)
            return HttpResponse('true')
        except Exception as e:
            return HttpResponse('false')

def userdel(request):
    id=request.POST.get('id')
    models.UserInfo.objects.filter(id=id).delete()
    return HttpResponse('true')

def useradd(request):
    if request.method=='GET':
        departs = models.Department.objects.all()
        roles = rbac_models.Role.objects.all()
        return render(request, 'user_add.html', {'departs': departs, 'roles': roles})
    if request.method=='POST':

        user_dict = json.loads(request.POST.get('data'))
        role_list = request.POST.getlist('role_list')

        name_list=['%s' %obj.name for obj in models.UserInfo.objects.all() ]
        if user_dict['username'] in name_list:
            return HttpResponse('exist') #表示用户已经存在
        else:
            try:
                models.UserInfo.objects.create(
                    name=user_dict['username'],
                    nickname=user_dict['nickname'],
                    phone=user_dict['phone'],
                    gender=user_dict['sex'],
                    email=user_dict['email'],
                    password=gen_md5(user_dict['pass']),
                    depart_id=models.Department.objects.filter(title=user_dict['depart']).first().id
                )
                obj=models.UserInfo.objects.filter(name=user_dict['username']).first()
                roleid_list = []
                for role in role_list:
                    roleid_list.append(rbac_models.Role.objects.filter(title=role).first().id)

                obj.roles.add(*roleid_list)
                return HttpResponse('true') #表示添加用户成功
            except Exception as e:
                return HttpResponse('false') #表示添加用户失败

