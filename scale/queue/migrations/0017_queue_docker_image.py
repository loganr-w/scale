# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-30 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queue', '0016_auto_20180123_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='docker_image',
            field=models.TextField(default=''),
        ),
    ]
