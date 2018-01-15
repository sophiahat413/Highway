# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_remove_record_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='interchange',
            new_name='inter',
        ),
        migrations.RenameField(
            model_name='record',
            old_name='latitude',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='record',
            old_name='longtitude',
            new_name='lon',
        ),
    ]
