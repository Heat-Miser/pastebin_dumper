# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Pastie(models.Model):
	scrape_url = models.CharField(max_length=255)
	full_url = models.CharField(max_length=255)
	date = models.DateTimeField()
	key = models.CharField(max_length=10, db_index=True)
	size = models.IntegerField()
	expire = models.DateTimeField(blank=True)
	title = models.CharField(max_length=255, blank=True)
	syntax = models.CharField(max_length=50)
	user = models.CharField(max_length=255, blank=True)

	def __str__(self): 
		return self.key

	class Meta:
		ordering = ["date"]