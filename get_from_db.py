import json


# -- get data from db
def get_data(connection, filter_word):
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

            pad_value = json.loads(cursor.fetchone()['value'])
            pad_text = pad_value['atext']['text']

            if (pad_text.split('\n')[0] != filter_word):
              # -- title
              pad_title = pad['key']

              # -- revision num
              pad_revisions = pad_value['head']

              # -- author num
              pad_authors = 0
              for item in pad_value['pool']['numToAttrib'].values():
                if item[0] == 'author':
                  pad_authors += 1

              # -- timestamp
              sql_pad_rev = "SELECT DISTINCT store.value FROM store WHERE store.key = %s"
              cursor.execute(sql_pad_rev, ('pad:' + pad['key'] + ':revs:' + str(pad_value['head']),))

              ts = json.loads(cursor.fetchone()['value'])['meta']['timestamp']
              pad_timestamp = ts

              # make tuple out of pad keys
              pad_item = (pad_title, pad_timestamp, pad_revisions, pad_authors)

              # -- add to list
              pad_list.append(pad_item)

          except Exception as e:
            print('parse pad err =>', e)

        return pad_list

  except Exception as e:
    print('db err =>', e)

  finally:
    cursor.close()
