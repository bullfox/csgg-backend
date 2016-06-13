import RiotAPI
import sys
import pprint
import time
import pymongo

max_depth = 6
user_ids = []
usernames = []
used_user_ids = []
used_game_ids = []
api = RiotAPI.riotAPI('e2a3eff8-772e-4e7a-a7c0-52edda53d1bc')

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def parse_WR(game):

    game_state = str(game['stats']['win'])
    game_state[0].upper()
    result = int(game_state == 'True') ^ int(game['stats']['team'] / 100)

    if result & 1:
        winner = 200
    else:
        winner = 100

    teamwin = []
    teamlose = []

    for player in game['fellowPlayers']:
        if player['teamId'] == winner:
            teamwin.append(player)
        else:
            teamlose.append(player)


    dbclient = pymongo.MongoClient()
    db = dbclient['countergg']
    collection = db['winratestest']
    posts = db.winrates

    for pwinner in teamwin:
        pwinner = pwinner['championId']
        for ploser in teamlose:
            ploser = ploser['championId']
            if (posts.find_one({'cid1' : int(pwinner), 'cid2' : int(ploser)}) != None):
                post = posts.find_one({'cid1' : int(pwinner), 'cid2' : int(ploser)})
                posts.update({'_id' : post['_id']}, {'$inc': {'c1wins' : int(1)}})
                if (posts.find_one({'cid1' : int(ploser), 'cid2' : int(pwinner)}) != None):
                    post = posts.find_one({'cid1' : int(ploser), 'cid2' : int(pwinner)})
                    posts.update({'_id' : post['_id']}, {'$inc': {'c2wins' : int(1)}})
                else:
                    posts.insert_one({'cid1' : int(ploser), 'cid2' : int(pwinner), 'c1wins' : 0, 'c2wins' : 1})
            else:
                posts.insert_one({'cid1' : int(pwinner), 'cid2' : int(ploser), 'c1wins' : 1, 'c2wins' : 0})

def get_Seeds(game):
    user_ids = []
    for i in game:
        user_ids.append(i['summonerId'])
    return user_ids

usernames = sys.argv
usernames.pop(0)
resume = usernames[0]
usernames.pop(0)
[username.lower() for username in usernames]

if resume == 1:
    with open('used_games', 'r') as used_games:
        for line in used_games:
            used_game_ids.append(line.strip('\n'));
    with open('used_ids', 'r') as used_ids:
        for line in used_ids:
            used_user_ids.append(line.strip('\n'));
    with open('user_ids', 'r') as user_ids:
        for line in user_ids:
            user_ids.append(line.strip('\n'));
else:
    for username in usernames:
        user_ids.append(api.summoner_by_name(username)[username]['id'])

id_number = 0

for i in range(1, max_depth):
    for user_id in [user_id for user_id in user_ids if user_id not in used_user_ids]:
        current_history = api.match_history(user_id)
        if current_history != None and 'games' in current_history:
            for game in current_history['games']:
                if game['subType'] == 'RANKED_SOLO_5x5' and game['gameId'] not in used_game_ids:
                    parse_WR(game)
                    user_ids += get_Seeds(game['fellowPlayers'])
                    used_user_ids.append(user_id)
                    used_game_ids.append(game['gameId'])
                    with open('used_ids', 'a') as used_ids:
                        for item in used_user_ids:
                            used_ids.write(str(item) + '\n')
                    with open('used_games', 'a') as used_games:
                        for item in used_game_ids:
                            used_games.write(str(item) + '\n')
                    with open('user_ids', 'a') as user_idfile:
                        for item in user_ids:
                            user_idfile.write(str(item) + '\n')
                            
        user_ids = list(set(user_ids) - set(used_user_ids))
                    
        id_number += 1
        sys.stdout.flush()
        restart_line()
        print("Number of id's trawled: " + str(id_number) + " and games: " + str(len(used_game_ids)), end="")

        time.sleep(1.3)
