# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-12-20 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0002_auto_20191220_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]
