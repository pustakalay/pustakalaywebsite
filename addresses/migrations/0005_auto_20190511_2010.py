# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-11 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_auto_20190505_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='nickname',
        ),
        migrations.AddField(
            model_name='address',
            name='address_name',
            field=models.CharField(blank=True, help_text='Name this address for Identification.', max_length=120, null=True),
        ),
    ]
