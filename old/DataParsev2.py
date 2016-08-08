import pymongo

class DataParse:
  def __init__(self, db_name, coll_name):
    self.dbclient = pymongo.MongoClient()
    self.db = self.dbclient[db_name]
    self.winrates = self.db[coll_name]
    self.stats = self.db['datastats2']
    self.statrecord = self.stats.find_one()
    
  def add_items(self, winner, loser, record):
    for i in range(1,7):
      itemid = str(winner['stats']['item' + str(i)]) 
      if 'c1items' in record and itemid in record['c1items']:
        self.winrates.update({'_id' : record['_id']}, {'$inc': {'c1items.' + itemid : int(1)}})
      else: 
        self.winrates.update({'_id' : record['_id']}, {'$set': {'c1items.' + itemid : 1}})
      itemid = str(loser['stats']['item' + str(i)])
      if 'c2items' in record and itemid in record['c2items']:
        self.winrates.update({'_id' : record['_id']}, {'$inc': {'c2items.' + itemid : int(1)}})
      else: 
        self.winrates.update({'_id' : record['_id']}, {'$set': {'c2items.' + itemid : 1}})
        
  def update_db(self, c1id, c2id, c1role, c2role, update, winner, loser):
    # Update the wins, adding new records if necessary
    if (self.winrates.find_one({'cid1' : c1id, 'c1role' : c1role,  'cid2' : c2id, 'c2role' : c2role}) != None): 
      record = self.winrates.find_one({'cid1' : c1id, 'c1role' : c1role,  'cid2' : c2id, 'c2role' : c2role})
      self.winrates.update({'_id' : record['_id']}, {'$inc': {update : int(1)}})
      # Update items if record exists
    else:
      self.winrates.insert_one({'cid1' : c1id, 'c1role' : c1role, 'cid2' : c2id, 'c2role' : c2role, 'c1wins' : 1, 'c2wins' : 0})
      record = self.winrates.find_one({'cid1' : c1id, 'c1role' : c1role, 'cid2' : c2id, 'c2role' : c2role, 'c1wins' : 1, 'c2wins' : 0})
    self.add_items(winner, loser, record)

  def store_matchups(self, game_Details):
    teams = self.determine_winners(game_Details)
    for winner in teams['0']:
      for loser in teams['1']:
        # Add to database stats
        self.stats.update({'_id' : self.statrecord['_id']}, {'$inc': {'matchups' : int(1)}})
        self.update_db(int(winner['championId']), int(loser['championId']), self.extract_role(winner), self.extract_role(loser), 'c1wins', winner, loser)
        self.update_db(int(loser['championId']), int(winner['championId']), self.extract_role(loser), self.extract_role(winner), 'c2wins', loser, winner)
                                      
  def extract_role(self, participant):
    if 'timeline' not in participant:
      return 'UNDEFINED'
    if participant['timeline']['role'] == 'SOLO' or participant['timeline']['role'] == 'NONE':
      return participant['timeline']['lane']
    elif participant['timeline']['role'] == 'DUO_CARRY':
      return 'ADC'
    else:
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