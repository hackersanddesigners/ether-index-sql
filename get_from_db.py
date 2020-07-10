import json


# -- get data from db
def get_data(connection):
  try:
    with connection.cursor() as cursor:
        # <https://github.com/ether/etherpad-lite/wiki/How-to-list-all-pads>
        sql_pads = "SELECT DISTINCT store.key, store.value FROM store WHERE store.key LIKE 'pad:%'"

        cursor.execute(sql_pads)
        pads = cursor.fetchall()

        pad_list = {}
        for pad in pads:
          try:
            # fetch text and authors num from key == `pad:<title>`
            # fetch revisions num and latest timestamp from `pad:<title>:revs:<num>`

            pad_key_split = pad['key'].split(':')

            if len(pad_key_split) == 2:
              pad_item = {'title': '',
                          'text': '',
                          'timestamp': 0,
                          'revisions': 0,
                          'authors': 0}

              pad_item['title'] = pad_key_split[1]

              pad_value = json.loads(pad['value'])
              pad_item['text'] = pad_value['atext']['text']

              for item in pad_value['pool']['numToAttrib'].values():
                if item[0] == 'author':
                  pad_item['authors'] += 1

              pad_list[pad_key_split[1]] = pad_item

            elif pad_key_split[2] == 'revs':
              pad_list[pad_key_split[1]]['revisions'] += 1
              pad_value = json.loads(pad['value'])
              if (int(pad_key_split[3]) == int(pad_list[pad_key_split[1]]['revisions']) - 1):
                pad_list[pad_key_split[1]]['timestamp'] = pad_value['meta']['timestamp']
          except Exception as e:
            print('parse pad err =>', e)

        # -- convert dict to tuple, so it's sortable and more flat
        padidx = [(v['title'], v['timestamp'], v['revisions'], v['authors']) for k, v in pad_list.items()]

        return padidx

  except Exception as e:
      print('db err =>', e)

  finally:
      cursor.close()
