# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CS', '0002_auto_20151004_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientservice',
            name='IpAddress',
            field=models.GenericIPAddressField(null=True, protocol='IPv4'),
        ),
    ]
