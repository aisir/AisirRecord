# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_remove_record_recorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='keywords',
            field=models.CharField(default='', max_length=200, verbose_name='关键词'),
        ),
        migrations.AddField(
            model_name='record',
            name='originalpage',
            field=models.TextField(default='', verbose_name='原文'),
        ),
    ]