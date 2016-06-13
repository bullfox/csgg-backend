URL = {
'base' : 'https://{region}.api.pvp.net/{url}',
'summoner_by_name' : 'api/lol/{region}/v{version}/summoner/by-name/{names}?api_key={api_key}',
'mastery_points' : 'championmastery/location/{region}/player/{id}/champions?api_key={api_key}',
'match_history' : 'api/lol/{region}/v{version}/game/by-summoner/{id}/recent?api_key={api_key}',
'game_details' : '/api/lol/{region}/v{version}/match/{id}?api_key={api_key}',
'match_list' : '/api/lol/{region}/v{version}/matchlist/by-summoner/{id}?beginTime={start_date}&api_key={api_key}',
'summoner_league' : '/api/lol/{region}/v{version}/league/by-summoner/{id}',
'item_details' : '/api/lol/static-data/{region}/v{version}/item?itemListData=into&api_key={api_key}',
'champion_details' : '/api/lol/static-data/{region}/v{version}/champion?api_key={api_key}'
}

VERSIONS = {
'summoner' : '1.4',
'mastery' : '1.2',
'history' : '1.3',
'game' : '2.2',
'matchlist' : '2.2',
'summoner' : '2.5',
'item' : '1.2',
'champion' : '1.2'
}

REGIONS = {
'euw' : 'euw',
'euw_alt' : 'EUW1',
'na' : 'na',
'global' : 'global'
}
