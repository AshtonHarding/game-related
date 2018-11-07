#!/bin/python2
import urllib, json, csv
from time import strftime

##
# Search API
# Inputs data
##

debug_mode = True
proceed = 0 # 0 is null, 1 is TRUE, 2 is FALSE

if debug_mode:
  print "-- DEBUG MODE ACTIVATED --"
  time_ran = strftime("%d/%b/%Y %I:%M %p")
  print 'Running at: '+str(time_ran)



def fetch_data():
  global users, users_id, api_key, ranger_one
  ## Variables ##
  api_key = '[REDACT]'
  users = ['Speedy Cerviche', 'Esperenza', 'MuteBoy', 'Berthold', 'MavDeath', 'lilira11']
  users_id = ['21177657', '488165', '44068247', '19394821', '46283982', '49267318']
  for ranger_one in range(0,6):
    print '----\n'
    search_api_one()




def search_api_one():
  global game_id, champion, game_mode, game_champ_id, api_one_last_game
  ## This searches for the last game
  if debug_mode:
    print 'searching for '+users[ranger_one]

  api_one_url = 'https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/'+users_id[ranger_one]+\
        '/recent?api_key='+api_key

  try:
    api_one_response = urllib.urlopen(api_one_url)
    api_one_data = json.loads(api_one_response.read())
  except Exception, e:
    print "ERROR CODE: "
    print e
  else:
    api_one_game_array = api_one_data['games']
    api_one_last_game = api_one_game_array[0] # EXTREMELY reliant on updates.
    game_id = api_one_last_game['gameId']
    game_champ_id = api_one_last_game['championId']

    check_game_type()
    check_champion_name()
    check_for_duplicates()



def check_game_type():
  ##
  # Game type check. (Format different outside of ranked)
  ##
  global proceed, game_mode
  if api_one_last_game['subType'] == 'RANKED_SOLO_5x5':
    proceed = 1
    game_mode = "Solo queue"
    if debug_mode:
      print api_one_last_game['subType']+' detected'
  elif api_one_last_game['subType'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5':
    proceed = 1
    game_mode = "Dynamic queue"
    if debug_mode:
      print api_one_last_game['subType']+' detected'
  elif api_one_last_game['subType'] == 'RANKED_TEAM_3x3':
    proceed = 2
    game_mode = "ranked 3s, still skipping."
    if debug_mode:
      print api_one_last_game['subType']+' detected'
  elif api_one_last_game['subType'] == 'RANKED_TEAM_5x5':
    # Doesn't really exist anymore
    proceed = 1
    game_mode = "ranked 5s"
    if debug_mode:
      print api_one_last_game['subType']+' detected'
  else:
    if debug_mode:
      print 'not ranked...Skipping.'
    proceed = 2



def check_champion_name():
  ##
  # Searching for the champion name (converting from the id)
  ##
  global champion
  item_map_int = {}
  with open('/home/kashire/code/projects/lol_db/champid.txt', 'r') as f:
    for line in f:
      splitLine = line.split()
      item_map_int[int(splitLine[0])] = " ".join(splitLine[1:])
  item_map_string = item_map_int.items() # Puts them in numerical order
  for champ_id, champ_name in item_map_string:
    if game_champ_id == champ_id:
      champion = champ_name
      if debug_mode:
        print 'playing: '+champion



def check_for_duplicates():
  ##
  # Check if game is a duplicate
  ##
  if proceed == 1:
    loc = '/home/kashire/code/projects/lol_db/csv/'+users[ranger_one]+'.csv'
    with open(loc, 'r') as f:
      reader = csv.reader(f)
      my_list = tuple(reader)
      if str(game_id) in str(my_list):
        print "Record exists. Skipping..."
      elif str(game_id) not in str(my_list):
        print "Record does not exist. Recording..."
        search_api_two()



def search_api_two():
  api_two_url ='https://na.api.pvp.net/api/lol/na/v2.2/match/'+str(game_id)+\
               '?includeTimeline=false&api_key='+str(api_key)
  if debug_mode:
    print "I made it to api_two"
  try:
    api_two_response = urllib.urlopen(api_two_url)
    api_two_data = json.loads(api_two_response.read())
  except Exception, e:
    print "No match found?"
  else:
    # For appending csv data
    target = open('/home/kashire/code/projects/lol_db/csv/'+users[ranger_one]+'.csv', 'a')
    # Find current user's participant id
    participants = api_two_data['participantIdentities'] # Looks bad, honestly.
    for player_id_search in range(0,10):
      if participants[player_id_search]['player']['summonerName'] == users[ranger_one]:
        if debug_mode:
          print "user located"

        ## The motherlode of data
        kills = api_two_data['participants'][player_id_search]['stats']['kills']
        deaths = api_two_data['participants'][player_id_search]['stats']['deaths']
        assists = api_two_data['participants'][player_id_search]['stats']['assists']
        cs = api_two_data['participants'][player_id_search]['stats']['minionsKilled']
        wards_placed = api_two_data['participants'][player_id_search]['stats']['wardsPlaced']
        wards_destroyed = api_two_data['participants'][player_id_search]['stats']['wardsKilled']
        damage_to_champs = api_two_data['participants'][player_id_search]['stats']['totalDamageDealtToChampions']
        game_length = api_two_data['matchDuration']
        game_min = (game_length / 60) # Minutes
        game_sec = (game_length % 60) # Seconds
        gold_zeroToTen = api_two_data['participants'][player_id_search]['timeline']['goldPerMinDeltas']['zeroToTen']
        ## tenToTwenty doesn't appear in json if it was shorter than 20mins.
        try:
          gold_tenToTwenty = api_two_data['participants'][player_id_search]['timeline']['goldPerMinDeltas']['tenToTwenty']
        except Exception:
          gold_tenToTwenty = "N/A"
        else:
          stupid = True
        if api_two_data['participants'][player_id_search]['stats']['winner'] == True:
          game_outcome = "Win"
        else:
          game_outcome = "Loss"
        date = strftime("%m/%d/%Y")
        comma = ', '
        ## data to string. Altered for convience.
        data_to_save = str(game_id) + comma +\
                       str(date) + comma +\
                       str(champion) + comma +\
                       str(kills) + comma +\
                       str(deaths) + comma +\
                       str(assists) + comma +\
                       str(cs) + comma +\
                       str(game_outcome) + comma +\
                       str(game_min)+':'+str(game_sec) + comma +\
                       str(gold_zeroToTen) + comma +\
                       str(gold_tenToTwenty) + comma +\
                       str(wards_placed) + comma +\
                       str(wards_destroyed) + comma +\
                       str(damage_to_champs) + comma +\
                       str(game_mode) + '\n'

        if debug_mode:
          print "saving: "+ data_to_save

        target.write(data_to_save)
        print "writing completed.\n"
        target.close() # closes the file
        break
