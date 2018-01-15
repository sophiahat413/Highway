# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
