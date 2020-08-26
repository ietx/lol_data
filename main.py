import urllib.request

header = 'https://br1.api.riotgames.com/lol/'

api_key = 'RGAPI-c210ab13-0e30-42d3-a318-90114054ad49'

query_type = 'summoner/v4/summoners/by-name/'

summoner_name = 'ietx'

url = header + query_type + summoner_name + '?api_key=' + api_key

data = urllib.request.urlopen(url)

print (data['id'])