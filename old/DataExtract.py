import pymongo

class DataParse:
  def extract_Matchups(self, current_Game):
    # Required list
    teams = []
    team_Win = []
    team_Lose = []
    teams.append(team_Win)
    teams.append(Team_Lose)
    # Determine winner
    self.determine_Winner(current_Game)
    # Initialise database connection
    dbclient = pymongo.MongoClient()
    db = dbclient['countergg']
    winrates = db.winrate2
    # Add players to respective teams
    self.add_Players(current_Game)
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

  def extract_Teammates(self, current_Game):
    
  def get_Game(self, current_Game):
    #Get game id and then call the full game method
      
  def determine_Winner(self, current_Game):
    game_State = str(current_Game['stats']['win'])
    game_State[0].upper()
    result = int(game_State == 'True') ^ int(current_Game['stats']['team'] / 100)
    if result & 1:
        return 200
    else:
        return 100
      
  def add_Players(self, current_Game):
    for player in current_Game['fellowPlayers']:
        if player['teamId'] == team_Win:
            teams[0].append(player['championId'])
        else:
            teams[1].append(player['championId'])
    winning_Team.append(current_Game['championId'])
    
  def extract_Players(self, current_Game):
    # Get users in current game and return them
    for player in current_Game['fellowPlayers']:
      user_Ids.append(player['summonerId'])
    return user_Ids