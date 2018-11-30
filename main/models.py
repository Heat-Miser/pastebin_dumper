# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Pastie(models.Model):
    scrape_url = models.CharField(max_length=255)
    full_url = models.CharField(max_length=255)
    date = models.DateTimeField()
    key = models.CharField(max_length=10, db_index=True)
    content = models.TextField(null=True)
    size = models.IntegerField()
    expire = models.DateTimeField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    syntax = models.CharField(max_length=50)
    user = models.CharField(max_length=255, blank=True)
    keep = models.BooleanField(default=False)

    def __str__(self):
        return self.key


class Pattern(models.Model):
    regex = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return self.comment

