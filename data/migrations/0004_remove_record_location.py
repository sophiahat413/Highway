# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_remove_record_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='location',
        ),
    ]
