# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-10 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile'),
        ),
    ]