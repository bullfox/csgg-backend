import pymongo

class DataParse:
  def __init__(self, db_name, coll_name):
    self.dbclient = pymongo.MongoClient(connect=False)
    # Initialise the winrates database
    self.db = self.dbclient[db_name]
    self.winrates = self.db[coll_name]
    self.winrates.drop()
    # Initialise the datastats database
    self.stats = self.db['datastats']
    self.stats.drop()
    self.stats.insert_one({'matchups' : 0})
    self.statrecord = self.stats.find_one()
    # Initialise the champion roles database
    self.champroles = self.db['champroles']
    self.champroles.drop()
    # Initialise the static database
    self.static = self.db['staticdata']
    self.itemdata = self.static.find({'type':'item'})


  def init_db(self, itemdata, champdata):
    # Store champdata in database
    champlist = []
    for key in champdata['data']:
      champlist.append(champdata['data'][key])
    newdict = {'champs' : champlist}
    self.static.insert(newdict)
    self.static.insert(itemdata)
    # Get the item details
    self.itemdata = itemdata
    self.dbclient.close()

  # Add the items
  def add_items(self, winner, loser, record):
    for i in range(1,7):
      itemid = str(winner['stats']['item' + str(i)])
      if (itemid != '0') and not ('group' in self.itemdata['data'][itemid]) and not ('into' in self.itemdata['data'][itemid]):
        if 'c1items' in record and itemid in record['c1items']:
          self.winrates.update({'_id' : record['_id']}, {'$inc': {'c1items.' + itemid : int(1)}})
        else:
          self.winrates.update({'_id' : record['_id']}, {'$set': {'c1items.' + itemid : 1}})
        itemid = str(loser['stats']['item' + str(i)])
      if (itemid != '0') and not ('group' in self.itemdata['data'][itemid]) and not ('into' in self.itemdata['data'][itemid]):
        if 'c2items' in record and itemid in record['c2items']:
           self.winrates.update({'_id' : record['_id']}, {'$inc': {'c2items.' + itemid : int(1)}})
        else:
           self.winrates.update({'_id' : record['_id']}, {'$set': {'c2items.' + itemid : 1}})

  def update_db(self, c1id, c2id, c1role, c2role, update, other, winner, loser):
    # Update the wins, adding new records if necessary
    if (self.winrates.find_one({'cid1' : c1id, 'c1role' : c1role,  'cid2' : c2id, 'c2role' : c2role}) != None):
      record = self.winrates.find_one({'cid1' : c1id, 'c1role' : c1role,  'cid2' : c2id, 'c2role' : c2role})
      self.winrates.update({'_id' : record['_id']}, {'$inc': {update : int(1)}})
      # Update items if record exists
    else:
      self.winrates.insert_one({'cid1' : c1id, 'c1role' : c1role, 'cid2' : c2id, 'c2role' : c2role, update : 1, other : 0})
      record = self.winrates.find_one({'cid1' : c1id, 'c1role' : c1role, 'cid2' : c2id, 'c2role' : c2role, update : 1, other : 0})
    self.add_items(winner, loser, record)

  def store_matchups(self, game_Details):
    teams = self.determine_winners(game_Details)
    for winner in teams['0']:
      for loser in teams['1']:
        # Add to database stats
        self.stats.update({'_id' : self.statrecord['_id']}, {'$inc': {'matchups' : int(1)}})
        self.update_db(int(winner['championId']), int(loser['championId']), self.extract_role(winner), self.extract_role(loser), 'c1wins', 'c2wins', winner, loser)
        self.update_db(int(loser['championId']), int(winner['championId']), self.extract_role(loser), self.extract_role(winner), 'c2wins', 'c1wins', loser, winner)

  def extract_role(self, participant):
    if 'timeline' not in participant:
      return 'UNDEFINED'
    if participant['timeline']['role'] == 'DUO_CARRY':
      if (self.champroles.find_one({'cid1' : participant['championId']}) != None):
        record = self.db.champroles.find_one({'cid1' : participant['championId']})
        self.db.champroles.update({'_id' : record['_id']}, {'$inc' : {'ADC' : int(1)}})
      else:
        self.champroles.insert({'cid1' : participant['championId'], 'TOP' : 0, 'JUNGLE' : 0, 'MIDDLE' : 0, 'SUPPORT' : 0, 'ADC' : 0})
        record = self.champroles.find_one({'cid1' : participant['championId']})
        self.champroles.update({'_id' : record['_id']}, {'$inc' : {'ADC' : int(1)}})
      return 'ADC'
    elif participant['timeline']['role'] == 'SOLO' or participant['timeline']['role'] == 'NONE':
      if (self.champroles.find_one({'cid1' : participant['championId']}) != None):
        record = self.champroles.find_one({'cid1' : participant['championId']})
        self.champroles.update({'_id' : record['_id']}, {'$inc' : {participant['timeline']['lane'] : int(1)}})
      else:
        self.champroles.insert({'cid1' : participant['championId'], 'TOP' : 0, 'JUNGLE' : 0, 'MIDDLE' : 0, 'SUPPORT' : 0, 'ADC' : 0})
        record = self.champroles.find_one({'cid1' : participant['championId']})
        self.champroles.update({'_id' : record['_id']}, {'$inc' : {participant['timeline']['lane'] : int(1)}})
      return participant['timeline']['lane']
    else:
      if (self.champroles.find_one({'cid1' : participant['championId']}) != None):
        record = self.champroles.find_one({'cid1' : participant['championId']})
        self.champroles.update({'_id' : record['_id']}, {'$inc' : {'SUPPORT' : int(1)}})
      else:
        self.champroles.insert({'cid1' : participant['championId'], 'TOP' : 0, 'JUNGLE' : 0, 'MIDDLE' : 0, 'SUPPORT' : 0, 'ADC' : 0})
        record = self.champroles.find_one({'cid1' : participant['championId']})
        self.champroles.update({'_id' : record['_id']}, {'$inc' : {'SUPPORT' : int(1)}})
      return 'SUPPORT'


  def determine_winners(self, game_Details):
    # Add players to their respective teams
    teams = {}
    teams['100'] = []
    teams['200'] = []
    for participant in game_Details['participants']:
        if (participant['teamId'] == 100):
            teams['100'].append(participant)
        else:
            teams['200'].append(participant)
    # Determine the winning team
    if (teams['100'][0]['stats']['winner']) == True:
      teams['0'] = teams['100']
      teams['1'] = teams['200']
    else:
      teams['1'] = teams['100']
      teams['0'] = teams['200']
    return teams

  def extract_players(self, game_Details):
    # Get userids from the current game
    user_Ids = []
    for participant in game_Details['participantIdentities']:
      user_Ids.append(participant['player']['summonerId'])
    return user_Ids
