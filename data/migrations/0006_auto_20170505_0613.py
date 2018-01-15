# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20170504_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='no',
            field=models.CharField(max_length=256),
        ),
    ]
