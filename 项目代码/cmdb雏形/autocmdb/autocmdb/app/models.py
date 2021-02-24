from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username=models.CharField(max_length=32)


class HostsInfo(models.Model):
    unique_id=models.CharField(max_length=32,unique=True)
    os_version = models.CharField(max_length=64)
    ip=models.CharField(max_length=32,unique=True)
    hostname=models.CharField(max_length=32)
    cpu=models.TextField()
    disk=models.TextField()
    main_board=models.TextField()
    memory=models.TextField()
    nic=models.TextField()


class HostConn(models.Model):
    ip=models.CharField(max_length=32,unique=True)
    port=models.CharField(max_length=32)
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    unique_id=models.CharField(max_length=32)


class HostTasks(models.Model):
    total=models.CharField(max_length=32)
    running=models.CharField(max_length=32)
    sleeping=models.CharField(max_length=32)
    stopped=models.CharField(max_length=32)
    zombie=models.CharField(max_length=32)
    host=models.ForeignKey('HostsInfo',to_field='id',on_delete=True)
    ctime=models.BigIntegerField()

class HostLoadavg(models.Model):
    one=models.CharField(max_length=32)
    five=models.CharField(max_length=32)
    fifteen=models.CharField(max_length=32)
    host=models.ForeignKey('HostsInfo', to_field='id', on_delete=True)
    ctime=models.BigIntegerField()


class HostCpu(models.Model):
    util=models.CharField(max_length=32)
    host=models.ForeignKey('HostsInfo', to_field='id', on_delete=True)
    ctime=models.BigIntegerField()


class HostMem(models.Model):
    total=models.CharField(max_length=32)
    used=models.CharField(max_length=32)
    buffcache=models.CharField(max_length=32)
    util=models.CharField(max_length=32)
    host=models.ForeignKey('HostsInfo', to_field='id', on_delete=True)
    ctime=models.BigIntegerField()


class HostSwap(models.Model):
    total=models.CharField(max_length=32)
    util=models.CharField(max_length=32)
    used=models.CharField(max_length=32)
    avail=models.CharField(max_length=32)
    host = models.ForeignKey('HostsInfo', to_field='id', on_delete=True)
    ctime=models.BigIntegerField()

class HostDisk(models.Model):
    device=models.CharField(max_length=32)
    rs=models.CharField(max_length=32)
    ws=models.CharField(max_length=32)
    rkBs=models.CharField(max_length=32)
    wkBs=models.CharField(max_length=32)
    io_util=models.CharField(max_length=32)
    total=models.CharField(max_length=32)
    used=models.CharField(max_length=32)
    size_util=models.CharField(max_length=32)
    host = models.ForeignKey('HostsInfo', to_field='id', on_delete=True)
    ctime = models.BigIntegerField()


class HostNic(models.Model):
    iface=models.CharField(max_length=32)
    rxpcks=models.CharField(max_length=32)
    txpcks=models.CharField(max_length=32)
    rxkbs=models.CharField(max_length=32)
    txkbs=models.CharField(max_length=32)
    rxcmps=models.CharField(max_length=32)
    txcmps=models.CharField(max_length=32)
    rxmcsts=models.CharField(max_length=32)
    host = models.ForeignKey('HostsInfo', to_field='id', on_delete=True)
    ctime=models.BigIntegerField()

