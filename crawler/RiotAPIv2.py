import RiotConsts as consts
import requests
import time

class RiotAPI:
    def __init__(self, user_key):
        self.api_key = user_key

    def request(self, url):
        url = consts.URL['base'].format(region = consts.REGIONS['euw'], url = url)
        response = None
        try:
            response = requests.get(url)
            return response.json()
        except:
            print('API Error')
            response = None

    def globalrequest(self, url):
        url = consts.URL['base'].format(region = consts.REGIONS['global'], url = url)
        response = None
        try:
            response = requests.get(url)
            print(url)
            return response.json()
        except:
            print('API Error')
            response = None

    def summoner_by_name(self, names):
        url = consts.URL['summoner_by_name'].format(region = consts.REGIONS['euw'], version = consts.VERSIONS['summoner'], names = names, api_key = self.api_key)
        return self.request(url)

    def mastery_points(self, id):
        url = consts.URL['mastery_points'].format(region = consts.REGIONS['euw_alt'], id = id, api_key = self.api_key)
        return self.request(url)

    def match_history(self, id):
        url = consts.URL['match_history'].format(region = consts.REGIONS['euw'], version = consts.VERSIONS['history'], id = id, api_key = self.api_key)
        return self.request(url)

    def game_details(self, id):
        url = consts.URL['game_details'].format(region = consts.REGIONS['euw'], version = consts.VERSIONS['game'], id = id, api_key = self.api_key)
        return self.request(url)

    def match_list(self, id, start_Date):
        url = consts.URL['match_list'].format(region = consts.REGIONS['euw'], version = consts.VERSIONS['matchlist'], id = id, start_date = start_Date, api_key = self.api_key)
        return self.request(url)

    def summoner_league(self, id):
        url = consts.URL['summoner_league'].format(region = consts.REGIONS['euw'], version = consts.VERSIONS['summoner'], id = id, api_key = self.api_key)
        return self.request(url)

    def item_details(self):
        url = consts.URL['item_details'].format(region = consts.REGIONS['euw'], version = consts.VERSIONS['item'], api_key = self.api_key)
        return self.globalrequest(url)

    def champion_details(self):
        url = consts.URL['champion_details'].format(region = consts.REGIONS['euw'], version = consts.VERSIONS['champion'], api_key = self.api_key)
        return self.globalrequest(url)
