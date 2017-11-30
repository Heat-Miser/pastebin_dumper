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
import tempfile
import shutil
import re

celery_app.conf.beat_schedule['update-every-two-seconds'] = {
    'task': 'main.tasks.list_new_pasties',
    'schedule': timedelta(seconds=2),
    'args': (),
}

celery_app.conf.beat_schedule['update-every-thirty-minutes'] = {
    'task': 'main.tasks.generate_proxies_list',
    'schedule': timedelta(minutes=30),
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

@celery_app.task
def generate_proxies_list():
	print "# Generating new proxies list"
	output_file = settings.PROXIES_LIST
	ip_regex = re.compile("(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]{1,5}")
	try:
		pastie = Pastie.objects.filter(user="spys1").latest("date")
		filename = "%s%s%s" % (settings.STORAGE_DIR, os.path.sep, pastie.key)

		with open(filename, 'r') as proxies_list:
			with tempfile.NamedTemporaryFile() as temp:
				counter = 0
				for line in proxies_list:
					for match in re.finditer(ip_regex, line):
						proxy = {'http': match.group()}
						try:
							r = requests.get("http://ifconfig.co/ip", proxies=proxy, timeout=1)
							ip = match.group().split(":")[0]
							if ip == r.text.strip():
								temp.write("%s\n" % (match.group()))
								counter += 1
						except:
							pass
				temp.flush()
				if counter > 0:
					shutil.copyfile(temp.name, output_file)
	except Exception as e:
		print "ERROR: unable to get proxies list"
		print e.message, e.args
		pass
