"""autocmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('signup/',views.signup),
    path('index/',views.index),
    path('forgot_password/',views.forgot_password),
    path('reset_password/',views.reset_password),
    path('hosts/',views.hosts),
    path('users/',views.users),
    path('roles/',views.roles),
    path('items/',views.items),
    path('add_roles/',views.add_roles),
    path('add_users/',views.add_users),
    re_path('host(?P<id>\d+)_detail/',views.host_detail),
    re_path('host(?P<id>\d+)_monitor/', views.host_monitor),
    path('mysql_detail/',views.mysql_detail),
    path('mysql_count/',views.mysql_count),
    path('add_morehosts/',views.add_morehosts),
    path('add_host/',views.add_host),
    path('flush_serverinfo/',views.flush_serverinfo),
    path('flush_minitorinfo/',views.flush_minitorinfo),
    path('get_monitor_data/',views.get_monitor_data)


]
