# Generated by Django 2.2.6 on 2020-03-25 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200325_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='ctime',
        ),
    ]
