# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CS', '0003_clientservice_ipaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientservice',
            name='ClientId',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='clientservice',
            name='ServiceId',
            field=models.CharField(max_length=100),
        ),
    ]
