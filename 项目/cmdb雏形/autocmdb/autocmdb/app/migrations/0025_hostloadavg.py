# Generated by Django 2.2 on 2019-09-06 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_hosttasks'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostLoadavg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one', models.CharField(max_length=32)),
                ('five', models.CharField(max_length=32)),
                ('fifteen', models.CharField(max_length=32)),
                ('host', models.ForeignKey(on_delete=True, to='app.HostsInfo')),
            ],
        ),
    ]
