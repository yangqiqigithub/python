# Generated by Django 2.2 on 2019-08-27 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_hostsinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostsinfo',
            old_name='mem_total',
            new_name='mem_info',
        ),
    ]
