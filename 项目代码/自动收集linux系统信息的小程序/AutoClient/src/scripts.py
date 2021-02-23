
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.client import AutoAgent

def client():
    try:
        cli = AutoAgent()
        cli.process()
    except  Exception as e:
        print(e)
