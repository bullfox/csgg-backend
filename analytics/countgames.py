import pymongo

dbclient = pymongo.MongoClient()
db = dbclient['countergg']
winrates = db.winrate2

games = 0

for doc in winrates.find():
    games += doc['c1wins']

games = games / 25
print(games)
