# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_auto_20161113_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='publish_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间'),
        ),
    ]
