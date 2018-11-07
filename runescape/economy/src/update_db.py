#!/usr/bin/env python2
#-*- coding: UTF-8 -*-

import urllib, json
import time

# WARNING: Due to the API throttling, this takes over 16+ hours to complete.

debug = False # You should know what this is for.

def get_info():
    for cat_num in range(0, 38):
        print "Searching in category " + str(cat_num)
        cat_URL = "http://services.runescape.com/m=itemdb_rs/api/"+\
                  "catalogue/category.json?category="
        print "Connecting to API-1.... (JaGeX throttles this... Please wait patiently..)"
        cat_response = urllib.urlopen(cat_URL + str(cat_num))
        cat_data = json.loads(cat_response.read())
        print "connected to API-1..."

        amount = []
        cat_type = cat_data['alpha']
        for x in range(1, 27):
            cat_group = cat_type[x]
            amount.append(cat_group['items'])

            page_limit = cat_group['items'] / 5 + 1
            page_limit = page_limit + 1
            if page_limit > 1:
                group_search_id = 12
            else:
                group_search_id = cat_group['items']

            # This is a fix for the "alpha" search... (Maybe change them all into variables.)
            if(cat_group['letter'] == '#'):
                cat_group_letter = "%23"
            else:
                cat_group_letter = cat_group['letter']

            print "cat group: " + str(x) + " in letter " + str(cat_group_letter) +\
                " contains " + str(cat_group['items']) + " items." + " | Pages: " +\
                str(page_limit)

            for rs_page in range(1, page_limit):
                group_url = "http://services.runescape.com/m=itemdb_rs/api/"+\
                "catalogue/items.json?category=" + str(cat_num) + "&alpha=" +\
                str(cat_group_letter) + "&page=" + str(rs_page)

                group_response = urllib.urlopen(group_url)
                group_data = json.loads(group_response.read())
                group_type = group_data["items"]

                if(debug == True):
                    for group_Num in range(0, group_search_id):
                        try:
                            group_stuff = group_type[group_Num]
                        except Exception, e:
                            pass
                        else:
                            print str(group_stuff['id']) + ' \t|\t ' +\
                                str(group_stuff['name'])
                if(debug == False):
                    with open("item_db.txt", "a") as itemFile:
                        for group_Num in range(0, group_search_id):
                            try:
                                group_stuff = group_type[group_Num]
                            except Exception, e:
                                pass
                            else:
                                itemFile.write(str(group_stuff['id']) + ' ' +\
                                        str(group_stuff['name']) + '\r\n')
                                print str(group_stuff['id']) + ' ' +\
                                        str(group_stuff['name'])

                print "[Just completed: page " + str(rs_page) + "]"
                time.sleep(5)

            print "[Just completed: letter " + str(cat_group_letter) + "]"

        print str(sum(amount)) + " items found in category " + str(cat_num)
        time.sleep(5)
        cat_num = cat_num + 1 # remove me.

print " -- Starting --\n This will take awhile....\n\n"
get_info()
print "\n-- Completed --"
