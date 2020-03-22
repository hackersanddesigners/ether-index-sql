import json


# -- get data from db
def get_data(connection):
  try:
    with connection.cursor() as cursor:
        # doing some pad.key trimming here, rather than below in the code.
        # <https://github.com/ether/etherpad-lite/wiki/How-to-list-all-pads>
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
            pad_v = json.loads(pad['value'])

            # -- set keys
            if ':revs:' not in pad['key']:
                padk = pad['key']
                pad_index[padk] = {'title': padk,
                                   'timestamp': 0,
                                   'revisions': 0,
                                   'authors': 0}

                for item in pad_v['pool']['numToAttrib'].values():
                    if item[0] == 'author':
                        pad_index[padk]['authors'] += 1
            else:
                pad_index[padk]['timestamp'] = pad_v['meta']['timestamp']
                pad_index[padk]['revisions'] += 1

        # -- convert dict to tuple, so it's sortable and more flat
        padidx = [(v['title'], v['timestamp'], v['revisions'], v['authors']) for k, v in pad_index.items()]

        return padidx

  except Exception as e:
      print('db err =>', e)

  finally:
      cursor.close()
