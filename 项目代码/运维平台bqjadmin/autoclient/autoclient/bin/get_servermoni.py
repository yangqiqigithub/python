#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASEDIR)
from core.servermonitor import ServerMoni
from core.client import AutoAgent


cli=AutoAgent()
cli.process(ServerMoni().get_servermoni())
