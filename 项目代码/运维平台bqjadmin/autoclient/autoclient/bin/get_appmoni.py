#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASEDIR)
from core.appmonitor import AppMoni
from core.client import AutoAgent

cli=AutoAgent()
cli.process(AppMoni().get_appmoni())