# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='record',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('longtitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('location', models.CharField(max_length=256)),
                ('no', models.IntegerField()),
                ('interchange', models.CharField(max_length=256)),
            ],
        ),
    ]
