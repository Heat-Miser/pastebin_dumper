import codecs
from celery import Celery
import requests

app = Celery('tasks')
app.conf.broker_url = "redis://localhost:6379/0"
app.conf.result_backend = 'redis://localhost:6379/0'


@app.task
def download_paste(id, output):
    url = "https://pastebin.com/api_scrape_item.php?i=%s" % (id)
    res = requests.get(url)
    f = codecs.open(output, "w", encoding='utf8')
    f.write(res.text)
    f.close()


