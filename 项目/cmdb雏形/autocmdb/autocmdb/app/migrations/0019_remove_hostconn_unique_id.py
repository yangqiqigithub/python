# Generated by Django 2.2 on 2019-08-29 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_hostconn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostconn',
            name='unique_id',
        ),
    ]
