# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20170505_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='no',
            field=models.IntegerField(),
        ),
    ]
