from __future__ import absolute_import, unicode_literals
from datetime import timedelta

import time
import json
import requests

from main.models import Pastie
from django.conf import settings

from pastebin_dumper.celery import app as celery_app

celery_app.conf.beat_schedule['update-every-one-minute'] = {
    'task': 'main.tasks.list_new_pasties',
    'schedule': timedelta(minutes=1),
    'args': (),
}


@celery_app.task
def list_new_pasties():
    print("# Getting new pasties")

    try:
        res = requests.get(settings.SCRAPING_URL)
        pasties = json.loads(res.text)
        for pastie in pasties:
            if Pastie.objects.filter(key=pastie["key"]).count() == 0:
                date = time.strftime('%Y-%m-%d %H:%M:%S+00:00', time.localtime(int(pastie["date"])))
                pastie["date"] = date
                expire = time.strftime('%Y-%m-%d %H:%M:%S+00:00', time.localtime(int(pastie["expire"])))
                pastie["expire"] = expire
                new_p = Pastie.objects.create(**pastie)
                downloading_new_pasties.delay(pastie["key"])
    except Exception as e:
        print("ERROR: unable to get new pasties")
        print(e.args)


@celery_app.task
def downloading_new_pasties(key):
    print(f"# Downloading new pastie {key}")
    try:
        new_p = Pastie.objects.get(key=key)
        res = requests.get(settings.SCRAPING_RAW_DATA_URL + key)
        new_p.content = res.text
        new_p.save()
    except Exception as e:
        print(f"ERROR: unable to download {key} pastie")
        print(e.args)


