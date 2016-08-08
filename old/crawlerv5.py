import RiotAPI
import sys
import time
import pymongo

# Usage is crawler KEY LIMIT DEPTH RESUME [SEEDS]
# Lists for seeds and trawled games + ids
seed_Users = []
used_Ids = []
user_Ids = []
used_Games = []
new_Users = []

# Deletes current line from stdout
def restart_Line():
    sys.stdout.write('\r')
    sys.stdout.flush()

# Extracts and stores winrates in the db
def extract_Data(current_Game):
    # Required lists
    winning_Team = []
    losing_Team = []
    user_Ids = []
    # Determine winner
    game_State = str(current_Game['stats']['win'])
    game_State[0].upper()
    result = int(game_State == 'True') ^ int(current_Game['stats']['team'] / 100)
    if result & 1:
        team_Win = 200
    else:
        team_Win = 100
    # Initialise database connection
    dbclient = pymongo.MongoClient()
    db = dbclient['countergg']
    winrates = db.winrate2
    # Add players to respective teams
    for player in current_Game['fellowPlayers']:
        if player['teamId'] == team_Win:
            winning_Team.append(player['championId'])
        else:
            losing_Team.append(player['championId'])
    winning_Team.append(current_Game['championId'])
    # Add results to database
    for winner in winning_Team:
        for loser in losing_Team:
            if (winrates.find_one({'cid1' : int(winner), 'cid2' : int(loser)}) != None):
                record = winrates.find_one({'cid1' : int(winner), 'cid2' : int(loser)})
                winrates.update({'_id' : record['_id']}, {'$inc': {'c1wins' : int(1)}})
            else:
                winrates.insert_one({'cid1' : int(winner), 'cid2' : int(loser), 'c1wins' : 1, 'c2wins' : 0})
            if (winrates.find_one({'cid1' : int(loser), 'cid2' : int(winner)}) != None):
                record = winrates.find_one({'cid1' : int(loser), 'cid2' : int(winner)})
                winrates.update({'_id' : record['_id']}, {'$inc': {'c2wins' : int(1)}})
            else:
                winrates.insert_one({'cid1' : int(loser), 'cid2' : int(winner), 'c1wins' : 0, 'c2wins' : 1})
    # Get users in current game and return them
    for player in current_Game['fellowPlayers']:
        user_Ids.append(player['summonerId'])
    return user_Ids

# Handling command line argument
clargs = sys.argv
clargs.pop(0)

# Api initialisation
api = RiotAPI.RiotAPI(clargs[0])
clargs.pop(0)

# Rate limit Setting
rate_Limit = float(clargs[0])
clargs.pop(0)

# Setting maximum depth
max_Depth = int(clargs[0])
clargs.pop(0)

# Whether to resume from saved details
if int(clargs[0]) == 1:
    # Open files and fill the used arrays with the details
    with open('used_games', 'r') as used_Games_File:
        for line in used_Games_File:
            used_Games.append(line.strip('\n'))
    with open('used_ids', 'r') as used_Ids_File:
        for line in used_Ids_File:
            used_Ids.append(line.strip('\n'))
    with open('user_ids', 'r') as user_Ids_File:
        for line in user_Ids_File:
            user_Ids.append(line.strip('\n'))
else:
    # Load rest of clargs as seed users
    clargs.pop(0)
    seed_Users = clargs
    [seed_User.lower() for seed_User in seed_Users]
    for seed_User in seed_Users:
        user_Ids.append(api.summoner_by_name(seed_User)[seed_User]['id'])

# Initialise number of ids and games crawled
ids_Crawled = 0
games_Crawled = 0

# Loop until at Maximum depth
for depth in range(max_Depth):
    # Loop through unused user ids
    for user_Id in user_Ids:
        # Get history for current user id
        current_History = api.match_history(user_Id)
        # If match history object returned successfully
        if (current_History != None) and ('games' in current_History):
            # For game in current history
            for current_Game in current_History['games']:
                # If game is ranked and unused
                if (current_Game['subType'] == 'RANKED_SOLO_5x5') and (current_Game['gameId'] not in used_Games):
                    # Parse game data and add to used lists
                    new_Users = extract_Data(current_Game)
                    user_Ids += new_Users
                    used_Ids.append(user_Id)
                    used_Games.append(current_Game['gameId'])
                    # Update used files
                    with open('used_games', 'a') as used_Games_File:
                        used_Games_File.write(str(current_Game['gameId']) + '\n')
                    with open('user_ids', 'a') as user_Ids_File:
                        for new_User in new_Users:
                            user_Ids_File.write(str(new_User) + '\n')
                    # Increment game counter
                    games_Crawled += 1
        # Remove duplicates from the user ids list
        user_Ids = list(set(user_Ids) - set(used_Ids))
        # Increment and print completed ids
        with open('used_ids', 'a') as used_Ids_File:
            used_Ids_File.write(str(user_Id) + '\n')
        ids_Crawled += 1
        sys.stdout.flush()
        restart_Line()
        print("Number of id's trawled: " + str(ids_Crawled) + " and games: " + str(games_Crawled), end="")
        # Sleep according to the rate limit
        time.sleep(rate_Limit)
