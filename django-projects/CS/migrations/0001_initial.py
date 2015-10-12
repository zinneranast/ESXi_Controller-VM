# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ClientId', models.IntegerField()),
                ('ClientName', models.CharField(max_length=50)),
                ('ClientSurname', models.CharField(max_length=50)),
                ('ClientEmail', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClientService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ClientId', models.ForeignKey(to='CS.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ServiceId', models.IntegerField()),
                ('ServiceName', models.CharField(max_length=50)),
                ('ServiceDescription', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='clientservice',
            name='ServiceId',
            field=models.ForeignKey(to='CS.Service'),
        ),
    ]
