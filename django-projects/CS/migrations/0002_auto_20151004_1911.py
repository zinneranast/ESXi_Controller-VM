# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='id',
        ),
        migrations.RemoveField(
            model_name='service',
            name='id',
        ),
        migrations.AlterField(
            model_name='client',
            name='ClientId',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='ServiceId',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
