# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 13:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_auto_20161115_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='recorder',
        ),
    ]
