# Generated by Django 2.2 on 2019-08-27 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_hostsinfo_ip'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HostsInfo',
        ),
    ]
