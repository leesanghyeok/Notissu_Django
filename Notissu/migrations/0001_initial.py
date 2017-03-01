# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword', models.CharField(max_length=100)),
                ('hash', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notice_id', models.IntegerField()),
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
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=500)),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notissu.Notice')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='keyword',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notissu.User'),
        ),
    ]
