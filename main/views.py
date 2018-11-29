# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse
from main.models import Pastie
import re
import os


def index(request):
    pattern = re.compile("^[a-zA-Z0-9]{8,16}$")
    number = Pastie.objects.count()
    if request.method == "GET":
        return render(request, "index.html",{"count": number}, RequestContext(request))
    elif request.method == "POST":
        key = request.POST["key"]
        if pattern.match(key):
            try:
                paste = Pastie.objects.get(key=key)
                response = HttpResponse(paste.content, content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(key)
                return response
            except:
                return render(request, "index.html",{"not_avaible": True, "count": number}, RequestContext(request))
        else:
            return render(request, "index.html",{"not_avaible": True, "count": number}, RequestContext(request))
