import pymongo

class DataParse:
  def __init__(self, db_name, coll_name):
    self.dbclient = pymongo.MongoClient()
    self.db = self.dbclient[db_name]
    self.winrates = self.db[coll_name]
    
  def store_matchups(self, game_Details):
    teams = self.determine_winners(game_Details)
    for winner in teams['0']:
      for loser in teams['1']:
        if (self.winrates.find_one({'cid1' : int(winner['championId']), 'c1role' : self.extract_role(winner),  'cid2' : int(loser['championId']), 'c2role' : self.extract_role(loser)}) != None):
          record = self.winrates.find_one({'cid1' : int(winner['championId']), 'c1role' : self.extract_role(winner), 'cid2' : int(loser['championId']), 'c2role' : self.extract_role(loser)})
          self.winrates.update({'_id' : record['_id']}, {'$inc': {'c1wins' : int(1)}})
        else:
          self.winrates.insert_one({'cid1' : int(winner['championId']), 'c1role' : self.extract_role(winner), 'cid2' : int(loser['championId']), 'c2role' : self.extract_role(loser), 'c1wins' : 1, 'c2wins' : 0})
          
        if (self.winrates.find_one({'cid1' : int(loser['championId']), 'c1role' : self.extract_role(loser), 'cid2' : int(winner['championId']), 'c2role' : self.extract_role(winner)}) != None):
          record = self.winrates.find_one({'cid1' : int(loser['championId']), 'c1role' : self.extract_role(loser), 'cid2' : int(winner['championId']), 'c2role' : self.extract_role(winner)})
          self.winrates.update({'_id' : record['_id']}, {'$inc': {'c2wins' : int(1)}})
        else:
          self.winrates.insert_one({'cid1' : int(loser['championId']), 'c1role' : self.extract_role(loser), 'cid2' : int(winner['championId']), 'c2role' : self.extract_role(winner), 'c1wins' : 0, 'c2wins' : 1})
      
  def determine_result(self, current_Participant):
    # Decide whether player won
    return (current_Participant['stats']['winner'])
                                      
  def extract_role(self, participant):
    if 'timeline' not in participant:
      print(participant)
    if participant['timeline']['role'] == 'SOLO' or participant['timeline']['role'] == 'NONE':
      return participant['timeline']['lane']
    elif participant['timeline']['role'] == 'DUO_CARRY':
      return 'ADC'
    else:
      return 'SUPPORT'
      
  def extract_players_teams(self, game_Details):
    # Add players to their respective teams
    teams = {}
    teams['100'] = []
    teams['200'] = []
    for participant in game_Details['participants']:
        if (participant['teamId'] == 100):
            teams['100'].append(participant)
        else:
            teams['200'].append(participant)
    return teams
  
  def determine_winners(self, game_Details):
    teams = self.extract_players_teams(game_Details)
    if self.determine_result(teams['100'][0]) == True:
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