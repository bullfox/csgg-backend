import json
import sys
import time
import pymongo

def matchwinrate(champ1, champ2):
    dbclient = pymongo.MongoClient()
    db = dbclient['countergg']
    winrates = db.winrate2

    c1wins = 0
    c2wins = 0

    if (winrates.find_one({'cid1' : int(champ1), 'cid2' : int(champ2)}) == None):
        print("Matchup not found")
    else:
        doc = winrates.find_one({'cid1' : int(champ1), 'cid2' : int(champ2)})
        c1wins = doc['c1wins']
        c2wins = doc['c2wins']

    return (c1wins / (c1wins + c2wins) * 100)


def getchamp(champ_name):
    with open('champdata.json') as sfile:
        champ_json = json.load(sfile)
        obj = champ_json['data'][champ_name]
    return(obj['id'])


print(matchwinrate(getchamp(sys.argv[1]), getchamp(sys.argv[2])))
