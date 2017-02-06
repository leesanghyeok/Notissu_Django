from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    contents = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=50)

class NoticeFiles(models.Model):
    id = models.AutoField(primary_key=True)
    noticeId = models.ForeignKey('Notice', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
