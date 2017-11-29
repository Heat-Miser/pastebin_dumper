import django
from django.conf import settings

django.setup()

from main.models import Pastie

from datetime import datetime, timedelta

from celery import Celery
import json
import requests
import codecs
import os
import time
import pytz

celeryapp = Celery(
    'pastebin_dumper',
    broker='redis://%s:%d/%d' % (settings.REDIS_HOST, settings.REDIS_PORT,
        settings.REDIS_DB),
    backend='redis://%s:%d/%d' % (settings.REDIS_HOST, settings.REDIS_PORT,
        settings.REDIS_DB)
    )


celeryapp.conf.beat_schedule['update-every-three-seconds'] = {
    'task': 'main.tasks.list_new_pasties',
    'schedule': timedelta(seconds=3),
    'args': (),
}


@celeryapp.task
def list_new_pasties():
	print "# Getting new pasties"
	
	if not os.path.exists(settings.STORAGE_DIR):
		print "Output directory does not exists... creating it !"
		os.makedirs(settings.STORAGE_DIR)

	try:
		res = requests.get(settings.SCRAPING_URL)
		pasties = json.loads(res.text)
		for pastie in pasties:
			if Pastie.objects.filter(key=pastie["key"]).count() == 0:
				date = time.strftime('%Y-%m-%d %H:%M:%S+00:00', time.localtime(int(pastie["date"])))
				pastie["date"] = date
				if pastie["date"] != "0":
					expire = time.strftime('%Y-%m-%d %H:%M:%S+00:00', time.localtime(int(pastie["expire"])))
				else:
					expire = ""
				pastie["expire"] = expire
				Pastie.objects.create(**pastie)
				filename = "%s/%s" % (settings.STORAGE_DIR, pastie["key"])
				downloading_new_pasties.delay(pastie["scrape_url"], pastie["key"], filename)
	except Exception as e:
		print e.message, e.args
		pass
			

@celeryapp.task
def downloading_new_pasties(url, key, output):
	print "# Downloading new pastie %s" % (key)
	res = requests.get(url)
	f = codecs.open(output, "w", encoding='utf8')
	f.write(res.text)
	f.close()

