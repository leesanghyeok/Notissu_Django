# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('contents', models.TextField(blank=True, null=True)),
                ('date', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NoticeFiles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=500)),
                ('noticeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notissu.Notice')),
            ],
        ),
    ]