# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Notissu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticefiles',
            name='notice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Notissu.Notice'),
        ),
    ]
