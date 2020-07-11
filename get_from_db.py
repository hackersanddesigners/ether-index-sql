import json


# -- get data from db
def get_data(connection):
  try:
    with connection.cursor() as cursor:
        # due to the way etherpad uses sql (eg, by dumping in in table with two columns all data, simply mapping the k,v json structure to sql)
        # it takes too much time and computation to keep in memory all the pads and then filter them in python
        # therefore:
        # - get list of pad titles
        # - get correct pad and fetch num of authors and of revisions (['head']: <num>)
        # - fetch correct pad-revs-<num> to get timestamp

        # <https://github.com/ether/etherpad-lite/wiki/How-to-list-all-pads>
        sql_pads = "SELECT DISTINCT SUBSTRING(store.key, 5, LOCATE(':', store.key, 5) -5) AS 'key' FROM store WHERE store.key LIKE 'pad:%'"

        cursor.execute(sql_pads)
        pads = cursor.fetchall()

        pad_list = []
        for pad in pads:
          try:
            sql_pad_value = "SELECT DISTINCT store.value FROM store WHERE store.key = %s"
            cursor.execute(sql_pad_value, ('pad:' + pad['key'],))

            pad_item = {'title': '',
                        'timestamp': 0,
                        'revisions': 0,
                        'authors': 0}

            # -- title
            pad_item['title'] = pad['key']

            t = cursor.fetchone()
            pad_value = json.loads(t['value'])

            # -- revision num
            pad_item['revisions'] = pad_value['head']

            # -- author num
            for item in pad_value['pool']['numToAttrib'].values():
              if item[0] == 'author':
                pad_item['authors'] += 1

            # -- timestamp
            sql_pad_rev = "SELECT DISTINCT store.value FROM store WHERE store.key = %s"
            cursor.execute(sql_pad_rev, ('pad:' + pad['key'] + ':revs:' + str(pad_value['head']),))

            ts = json.loads(cursor.fetchone()['value'])['meta']['timestamp']
            pad_item['timestamp'] = ts

            # -- add to list
            pad_list.append(pad_item)

          except Exception as e:
            print('parse pad err =>', e)

        # -- convert list of dictionaries to list of tuples, so it's sortable and more flat
        pad_index = [(pad['title'], pad['timestamp'], pad['revisions'], pad['authors']) for pad in pad_list]
        return pad_index

  except Exception as e:
      print('db err =>', e)

  finally:
      cursor.close()
