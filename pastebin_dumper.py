import json
import requests
import time
import sqlite3
import os
from async_downloader import download_paste

API_URL="https://pastebin.com/api_scraping.php?limit=100"
OUTPUT_DIRECTORY="downloaded_pasties"
DB_NAME="pastedumper.sqlite"


def create_db(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("CREATE TABLE pasties (url text, date int, key text, size int, expire int, title text, syntax text, user text)")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    print "### STARTING PASTEBIN DUMPER"

    if not os.path.exists(DB_NAME):
        print "DB does not exists... creating a new one !"
        create_db(DB_NAME)
    if not os.path.exists(OUTPUT_DIRECTORY):
        print "Output directory does not exists... creating it !"
        os.makedirs(OUTPUT_DIRECTORY)
    
    print "Connecting to DB"
    db_handle = sqlite3.connect(DB_NAME)
    db_cursor = db_handle.cursor()

    print "Full setup ok... let's run !"
    while True:
        res = requests.get(API_URL)
        try:
            pasties = json.loads(res.text)
            for pastie in pasties:
                db_cursor.execute('SELECT 1 FROM pasties WHERE key=? LIMIT 1', (pastie["key"],))
                if db_cursor.fetchone() is None:
                    filename = "%s/%s" % (OUTPUT_DIRECTORY, pastie["key"])
                    download_paste.delay(pastie["key"], filename)
                    values = (pastie["full_url"],
                                int(pastie["date"]),
                                pastie["key"],
                                int(pastie["size"]),
                                int(pastie["expire"]),
                                pastie["title"],
                                pastie["syntax"],
                                pastie["user"])
                    db_cursor.execute('INSERT INTO pasties VALUES(?,?,?,?,?,?,?,?)', values)
                    db_handle.commit()
                    filename = "%s/%s" % (OUTPUT_DIRECTORY, pastie["key"])
            time.sleep(3)
        except (KeyboardInterrupt, SystemExit):
            print "Quitting... bye !"
            db_handle.close()
            exit(0)
        except Exception as e:
            print e.message, e.args
            pass
