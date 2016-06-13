import pymongo
import sys
import time
import RiotAPIv2
import DataParse

# Required lists
seed_Users = []
used_Ids = []
user_Ids = []
used_Games = []
match_List = []
top_Seeds = []
  
# Handling command line arguments
clargs = sys.argv

# Api initialisation
api = RiotAPIv2.RiotAPI(clargs[1])
parse = DataParse.DataParse('countergg', 'winrates3')

# Rate limit Setting
rate_Limit = float(clargs[2])

# Patch date in unix time
patch_Date = int(clargs[3])

# Get starting point
seed_Users.append(21999355)

# if toplist not there or time has not passed
# Generate more people in the traditional way
# otherwise, go through the list for games
# increase people's score

while(1):
  # If 2 days has not elapsed or topseeds doesn't exist crawl normally
  if (time.time() - last_Check) < 172800 or not (top_Seeds):
    seed_Users = crawled_Seeds
  else:
    last_Check = time.time()
    seed_Users = top_Seeds
  for seed_User in seed_Users:
    # Get matchlist
    match_List = api.match_list(seed_User, patch_Date)
    used_Ids.append(seed_User)
    # Initialise games from single user
    games_From_Seed = 0
    if 'matches' in match_List
      for match in match_List['matches']:
        if (match['region'] =='EUW') and (match['matchId'] not in used_Games):
          # Get details
          game_Details = api.game_details(match['matchId'])
          # Increment games obtained from user
          games_From_Seed += 1
          if 'participants' in game_Details: 
            # Call parsing scripts
            parse.store_matchups(game_Details)
            # Add to completed lists
            seed_Users += parse.extract_players(game_Details)
            used_Games.append(match['matchId'])
            # Comply with rate limit
            time.sleep(rate_Limit)
            # Calculate top seeds data
            # If can't find user in list
              # Append them
            # E;se
              # Add their score to the second column
    
    # Remove reoccurances from lists
    print("Summoner id: " + str(seed_User) + ', games: ' + games_From_Seed + ', total games: ' + str(len(used_Games)))
    used_Ids = list(set(used_Ids))
    seed_Users = list(set(seed_Users) - set(used_Ids))
      