#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.urls import path,include,re_path
from django.contrib import admin
from rbac.views import role
from rbac.views import user
from rbac.views import menu
#以下是django2的路径写法，django1用的是url
urlpatterns = [

    path('role/list/', role.role_list, name='role_list'),  # rbac:role_list
    path('role/add/', role.role_add, name='role_add'),  # rbac:role_add
    re_path('role/edit/(?P<pk>\d+)/', role.role_edit, name='role_edit'),  # rbac:role_edit
    re_path('role/del/(?P<pk>\d+)/', role.role_del, name='role_del'),  # rbac:role_del

    # url(r'^user/list/$', user.user_list, name='user_list'),
    # url(r'^user/add/$', user.user_add, name='user_add'),
    # url(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),  # rbac:user_edit
    # url(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),
    # url(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),


    #
    re_path('second/menu/add/(?P<menu_id>\d+)/', menu.second_menu_add, name='second_menu_add'),
    re_path('second/menu/edit/(?P<pk>\d+)/', menu.second_menu_edit, name='second_menu_edit'),
    re_path('second/menu/del/(?P<pk>\d+)/', menu.second_menu_del, name='second_menu_del'),

    path('menu/list/', menu.menu_list, name='menu_list'),
    path('menu/add/', menu.menu_add, name='menu_add'),
    re_path('menu/edit/(?P<pk>\d+)/', menu.menu_edit, name='menu_edit'),
    re_path('menu/del/(?P<pk>\d+)/', menu.menu_del, name='menu_del'),


    re_path('permission/add/(?P<second_menu_id>\d+)/', menu.permission_add, name='permission_add'),
    re_path('permission/edit/(?P<pk>\d+)/', menu.permission_edit, name='permission_edit'),
    re_path('permission/del/(?P<pk>\d+)/', menu.permission_del, name='permission_del'),

    path('multi/permissions/', menu.multi_permissions, name='multi_permissions'),
    re_path('multi/permissions/del/(?P<pk>\d+)/', menu.multi_permissions_del, name='multi_permissions_del'),

    path('distribute/permissions/', menu.distribute_permissions, name='distribute_permissions'),

]
