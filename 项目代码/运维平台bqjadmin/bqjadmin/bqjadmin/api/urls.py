#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang

from django.urls import path
from api import views
urlpatterns = [
    path('asset/',views.asset),
]


