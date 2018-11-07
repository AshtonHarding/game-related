#!/usr/bin/env python2
#-*- coding: UTF-8 -*-

import urllib
import json
from time import time

def title_intro():
  print ''
  print "########################################"
  print "#   The Runescape economy tracker      #"
  print "#   | version 1.04               |     #"
  print "########################################"
  print "#   created by: Kashire                #"
  print "#   https://github.com/AshtonHarding   #"
  print "#   reddit: ashton_harding             #"
  print "########################################"
  print ''

def make_selection():
  global url
  selection = raw_input('Please select: {OSRS} or {RS3} : ').lower()
  if selection == "osrs":
    url = "http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item="
    find_item()
  elif selection == "rs3":
    url = "http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item="
    find_item()
  else:
    print "Error: " + selection + " does not exist. Did you make a typo?"

#!/bin/bash
import urllib, json
from time import time

t0 = time()

def title_intro():
  print ''
  print "########################################"
  print "#   The Runescape economy tracker      #"
  print "#   | version 1.04               |     #"
  print "########################################"
  print "#   created by: Kashire                #"
  print "#   https://github.com/AshtonHarding   #"
  print "#   reddit: ashton_harding             #"
  print "########################################"
  print ''

def make_selection():
  global url
  selection = raw_input('Please select: {OSRS} or {RS3} : ').lower()
  if selection == "osrs":
    url = "http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item="
    find_item()
  elif selection == "rs3":
    url = "http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item="
    find_item()
  else:
    print "Error: " + selection + " does not exist. Did you make a typo?"

def find_item():
    # dictionary (finds the id)!
  item_map_int = {}
  with open('item_db.txt', 'r') as f:
    for line in f:
      splitLine = line.split()
      item_map_int[int(splitLine[0])] = " ".join(splitLine[1:])

  item_map_string = {v: k for k, v in item_map_int.items()}

  rs_item_array_search = []
  try:
    rs_item_amount = input('How many items should I look up? : ')
  except Exception, e:
    print "That is not a valid number."
  else:

    for x in range(0, rs_item_amount):
      rs_item_names_to_search = raw_input("Item #" + str(x) +' : ')
      rs_item_array_search.append(str(rs_item_names_to_search))

    for y in range(0, rs_item_amount):
    #  print rs_item_array_search[y]
      try:
        rs_item_number = item_map_string[rs_item_array_search[y].capitalize()]
      except Exception, e:
        print str(e) + " is not an item name."
      else:

        print "searching database...(" + str(y) + "/" + str(rs_item_amount) + ")"

        rs_response = urllib.urlopen(url+str(rs_item_number))
        rs_data = json.loads(rs_response.read())
        #t2 = time() # The API is seriously slow. Might need to make a better scrape.
        print "item located."

        # Data structures galore.
        rs_item_db_array = rs_data['item']            # Structure{Item_Info}
        rs_item_name = rs_item_db_array['name']       # item name
        rs_item_id = rs_item_db_array['id']           # item ID
        rs_item_current = rs_item_db_array['current'] # Structure{current}
        rs_item_cost = rs_item_current['price']       # item price
        rs_item_member = rs_item_db_array['members']  # Is it memebers? (Spit true/false)

        rs_day0_box = rs_item_db_array['today']
        rs_day0_price_change = rs_day0_box['price']

        rs_day30_box = rs_item_db_array['day30']
        rs_day30_trend = rs_day30_box['change']

        rs_day90_box = rs_item_db_array['day90']
        rs_day90_trend = rs_day90_box['change']

        rs_day180_box = rs_item_db_array['day180']
        rs_day180_trend = rs_day180_box['change']

        print '\n' + \
          'item name: [' + str(rs_item_name) + ']\n' + \
          'item id:   [' + str(rs_item_id) + ']\n' + \
          'item cost: [' + str(rs_item_cost) + '] gp\n' + \
          'today:     [' + str(rs_day0_price_change) + '] gp\n' \
          'members:   [' + str(rs_item_member) + ']\n' + \
          '030 day:   [' + str(rs_day30_trend) + ']\n' + \
          '090 day:   [' + str(rs_day90_trend) + ']\n' + \
          '180 day:   [' + str(rs_day180_trend) + ']\n'

title_intro()
make_selection()

