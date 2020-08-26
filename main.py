import urllib.request, json

header = 'https://br1.api.riotgames.com/lol/'

api_key = 'RGAPI-c210ab13-0e30-42d3-a318-90114054ad49'

query_type = 'summoner/v4/summoners/by-name/'

summoner_name = 'ietx'

url = header + query_type + summoner_name + '?api_key=' + api_key

response = urllib.request.urlopen(url)

data = json.loads(response.read())

player_id = data['id']

print(player_id)


response = urllib.request.urlopen('http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json')
data = json.loads(response.read())
data['data']['Neeko']
