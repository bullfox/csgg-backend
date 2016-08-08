URL = {
'base' : 'https://{region}.api.pvp.net/{url}',
'summoner_by_name' : 'api/lol/{region}/v{version}/summoner/by-name/{names}?api_key={api_key}',
'mastery_points' : 'championmastery/location/{region}/player/{id}/champions?api_key={api_key}',
'match_history' : 'api/lol/{region}/v{version}/game/by-summoner/{id}/recent?api_key={api_key}',
'game_details' : '/api/lol/{region}/v{version}/match/{id}?api_key={api_key}',
'match_list' : '/api/lol/{region}/v{version}/matchlist/by-summoner/{id}?rankedQueues=RANKED_SOLO_5x5&endIndex=25&api_key={api_key}',
'summoner_league' : '/api/lol/{region}/v{version}/league/by-summoner/{id}'
}

VERSIONS = {
'summoner' : '1.4',
'mastery' : '1.2',
'history' : '1.3',
'game' : '2.2',
'matchlist' : '2.2'
'summoner' : '2.5'
}

REGIONS = {
'euw' : 'euw',
'euw_alt' : 'EUW1',
'na' : 'na'
}
