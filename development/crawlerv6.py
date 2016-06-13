import pymongo
import sys
import time
import RiotAPIv2
import DataParsev21

# Required lists
seed_Users = []
used_Ids = []
user_Ids = []
used_Games = []
match_List = []
  
# Handling command line arguments
clargs = sys.argv

# Api initialisation
api = RiotAPIv2.RiotAPI(clargs[1])
parse = DataParsev21.DataParse('countergg', 'winrates')

# Rate limit Setting
rate_Limit = float(clargs[2])

# Patch date in unix time
patch_Date = int(clargs[3])

# Get starting point
seed_Users.append(21999355)

# Initialise the reference data
parse.init_json(api.item_details(), api.champion_details())

for i in range(10):
  for seed_User in seed_Users:
    # Get matchlist
    match_List = api.match_list(seed_User, patch_Date)
    # If request didn't work then skip loop iteration
    if match_List == None:
      continue
    used_Ids.append(seed_User)
    if 'matches' in match_List:
      for match in match_List['matches']:
        if (match['region'] =='EUW') and (match['matchId'] not in used_Games):
          # Get details
          game_Details = api.game_details(match['matchId'])
          # If request didn't work then skip loop iteration
          if game_Details == None:
            continue
          if 'participants' in game_Details: 
            # Call parsing scripts
            parse.store_matchups(game_Details)
            # Add to completed lists
            seed_Users += parse.extract_players(game_Details)
            used_Games.append(match['matchId'])
            time.sleep(1.8)
    
    # Comply with rate limit
    # Remove reoccurances from lists
    print("Summoner id: " + str(seed_User) + ', games: ' + str(len(used_Games)))
    used_Ids = list(set(used_Ids))
    seed_Users = list(set(seed_Users) - set(used_Ids))