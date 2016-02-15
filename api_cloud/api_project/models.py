# -*- coding:utf8 -*-
from django.db import models


# Create your models here.
class ApiProject(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, default=1)
    api_document = models.CharField(max_length=1000, blank=True, null=True)
    status = models.IntegerField(blank=True, default=1)
    create_time = models.DateTimeField(blank=True)
