from __future__ import absolute_import, unicode_literals

from main.models import Pastie

from datetime import datetime, timedelta
from pastebin_dumper.celery import app as celery_app
from django.conf import settings
import json
import requests
import codecs
import os
import time

celery_app.conf.beat_schedule['update-every-three-seconds'] = {
    'task': 'main.tasks.list_new_pasties',
    'schedule': timedelta(seconds=3),
    'args': (),
}

@celery_app.task
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
		print "ERROR: unable to get new pasties"
		print e.message, e.args
		pass
			

@celery_app.task
def downloading_new_pasties(url, key, output):
	print "# Downloading new pastie %s" % (key)
	try:
		res = requests.get(url)
		f = codecs.open(output, "w", encoding='utf8')
		f.write(res.text)
		f.close()
	except Exception as e:
		print "ERROR: unable to download %s pastie" % (key)
		print e.message, e.args
		pass

