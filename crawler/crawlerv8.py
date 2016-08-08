import pymongo
import sys
import time
import RiotAPIv2
import DataParsev21
from multiprocessing import Pool
from itertools import repeat

def process_Seed(seed_User, api, used_Games):
    temp_Seeds = []
    return_List = []
    return_List.append(0)
    match_List = api.match_list(seed_User, 1470182400000)
    if (match_List == None) or ('matches' not in match_List):
        return
    for match in match_List['matches']:
        if (match['region'] == 'EUW') and (match['matchId'] not in used_Games):
            game_Details = api.game_details(match['matchId'])
            if ('status' in game_Details):
                print(game_Details['status']['status_code'])
                continue
            print(match['matchId'])
            return_List[0] += 1
            temp_Seeds += parse.extract_players(game_Details)
            if (game_Details == None) or ('participants' not in game_Details):
                continue
            return_List.append(match['matchId'])
            parse.store_matchups(game_Details)
    return_List += temp_Seeds
    return return_List

# Required lists
current_Seeds = []
all_Seeds = []
used_Games = []
top_Seeds = []

# Handling command line arguments
clargs = sys.argv

# Api initialisation
api = RiotAPIv2.RiotAPI(clargs[1])

# Get starting point
all_Seeds.append(21999355)

last_Check = time.time()
parse = DataParsev21.DataParse('countergg', 'winrates')
parse.init_db(api.item_details(), api.champion_details())

while(1):
# TOP SEEDS IS NOT INTEGRATED
#    if (last_Check - time.time() > 172800):
#        all_Seeds.insert(top_Seeds, seed_Index)
#        last_Check = time.time()

    current_Seeds = all_Seeds[:100]
    all_Seeds = all_Seeds[100:]
    p = Pool(5)
    process_Returns = p.starmap(process_Seed, zip(current_Seeds, repeat(api), repeat(used_Games)))
    print(process_Returns)
    # Return takes this format:
    # first place how many games found
    # Used game ids until done
    # Rest seed users
    for l in process_Returns:
        if l == None:
            continue
        used_Games += l[1:l[0]+1]
        all_Seeds += l[l[0]+1:]
