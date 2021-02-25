#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASEDIR)
from core.serverinfo import ServerInfo
from core.client import AutoAgent

cli=AutoAgent()
cli.process(ServerInfo().get_serverinfo())

