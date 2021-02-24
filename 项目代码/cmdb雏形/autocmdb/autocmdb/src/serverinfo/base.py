#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib.log import Logger
import traceback
class BasePlugin():

    def __init__(self,host_dict):
        self.logger = Logger()
        self.host_dict=host_dict
        self.hostname=self.os_hostname()


    @property
    def ssh(self):
        host_dict=self.host_dict
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            ssh.connect(hostname=host_dict['ip'],port=host_dict['port'], username=host_dict['username'], password=host_dict['password'])
        except Exception as e:
            msg = "%s linux BasePlugin-ssh connect  error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
        return ssh


    def os_hostname(self):
        """
        获取主机名
        :return:
        """
        stdin, stdout, stderr = self.ssh.exec_command('hostname')
        hostname = stdout.read().decode('gbk').strip()
        return hostname

    def linux(self):
        raise Exception('You must implement linux method.')

