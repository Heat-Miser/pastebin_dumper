# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from main.models import Pastie

# Create your views here.
def index(request):
	res = ""
	for pastie in Pastie.objects.all():
		res += "%s<br>" % (pastie.key)
	return HttpResponse(res)