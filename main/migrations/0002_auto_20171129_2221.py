# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastie',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='pastie',
            name='expire',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='pastie',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='pastie',
            name='user',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
