"""bqjadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path,include,re_path
from cmdb.views import show_hosts
from cmdb.views import account
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('rbac/', include(('rbac.urls','rbac'), namespace='rbac')),
    path('index/', account.index,name='index'),
    path('hosts/', show_hosts.show_hosts,name='hosts'),
    re_path('hosts/hostinfo/(\d+)', show_hosts.hostinfo,name='hostsinfo'),
    path('get_hosts_json/', show_hosts.get_hosts_json,name='get_hosts_json'),
    path('hostToitem/', show_hosts.hostToitem,name='hostToitem'),
    path('dbToitem/', show_hosts.dbToitem,name='dbToitem'),
    path('login/', account.login,name='login'),
    path('logout/', account.logout,name='logout'),
    re_path('userinfo/(\d+)', account.userinfo,name='userinfo'),
    path('users/', account.show_users,name='show_users'),
    path('dbs/', show_hosts.show_dbs,name='show_dbs'),
    re_path('users/useredit/(\d+)', account.user_edit,name='user_edit'),
    path('test/', account.test,name='test'),
    path('users/userdel/',account.userdel,name='userdel'),
    path('users/useradd/',account.useradd,name='useradd'),
    path('get_json_user/',account.get_json_user,name='get_json_user'),
    path('get_dbs_json/',show_hosts.get_dbs_json,name='get_dbs_json')





]
