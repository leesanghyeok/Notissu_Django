# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    notice_id = models.IntegerField()
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    contents = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=50)


class NoticeFiles(models.Model):
    id = models.AutoField(primary_key=True)
    notice_id = models.IntegerField()
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=200)


class Keyword(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)
