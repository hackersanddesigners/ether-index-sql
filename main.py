import json
import pymysql.cursors
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime

# create .env file path.
dotenv_path = join(dirname(__file__), '.env')
# load file from the path.
load_dotenv(dotenv_path)

connection = pymysql.connect(host=os.getenv('DB_HOST'),
                             user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASSWORD'),
                             db=os.getenv('DB_NAME'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql_pads = "SELECT DISTINCT SUBSTRING(store.key,5) AS 'key', store.value FROM store WHERE store.key LIKE 'pad:%'"
        cursor.execute(sql_pads)
        pads = cursor.fetchall()

        # from store.values get:
        # - pad's number of revisions
        # - pad's latest timestamp
        # - pad's number of authors

        # set unique keys in dictonary for each pad
        pad_index = {}
        for pad in pads:
            if ':revs:' in pad['key']:
                padk = pad['key'].split(':')[0]
                pad_index[padk] = {'revisions': 0,
                                   'timestamp': 0,
                                   'authors': 0}

        # count pad.key to calculate revision # for each unique key
        for pad in pads:
            padk = pad['key'].split(':')[0]
            pad_v = json.loads(pad['value'])
            try:
                ts = pad_v['meta']['timestamp']
                pad_index[padk]['revisions'] += 1
                pad_index[padk]['timestamp'] = ts
            except Exception as e:
                print('pad has no key', e)
                for item in pad_v['pool']['numToAttrib'].values():
                    if item[0] == 'author':
                        pad_index[padk]['authors'] += 1

        print('pads-index', pad_index)

finally:
    connection.close()
