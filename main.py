import urllib.request
import json
import requests

import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO


api_key = 'RGAPI-f04af0c5-dae9-4686-ab07-e0af39954ef5'

summoner_name = 'ietx'

regions = {
'BR': 'br1',
'EUN': 'eun1',
'EUW': 'euw1',
'JP': 'jp1',
'KR': 'kr',
'LA1': 'la1',
'LA2': 'la2',
'OC': 'oc1',
'RU': 'ru',
'TR1': 'tr1'
}

query_type = {
'summoner_info': 'summoner/v4/summoners/by-name/',
'mastery': 'champion-mastery/v4/champion-masteries/by-summoner/'
}

def head(region):
    return 'https://' + region + '.api.riotgames.com/lol/'

def tail(api_key):
    return '?api_key=' + api_key

def make_url(*args):
    joined_args = ''
    for arg in args:
        joined_args += arg
    return joined_args

def request(url):
    return urllib.request.urlopen(url).read()

def extract_json(url):
    return json.loads(request(url))

def get_image(url):
    return Image.open(BytesIO(request(url)))

def print_img(image):
    plt.imshow(image)
    plt.axis('off')
    plt.show()

champions_data = extract_json(data_dragon[0])
def champion_id_name(champions_data):
    champion_names = list(champions_data['data'].keys())
    champion_name_to_id = {}
    for name in champion_names:
        champion_name_to_id[name] = int(champions_data['data'][name]['key'])
    champion_id_to_name = {v: k for (k, v) in champion_name_to_id.items()}
    return champion_name_to_id, champion_id_to_name
champion_name_to_id, champion_id_to_name = champion_id_name(champions_data)

class playerId():

    def __init__(self, *args):
        url = make_url(*args)
        self.raw_data = json.loads(urllib.request.urlopen(url).read())
        self.id = self.raw_data['id']
        self.account_id = self.raw_data['accountId']
        self.puu_id = self.raw_data['puuid']
        self.name = self.raw_data['name']
        self.profile_icon_id = self.raw_data['profileIconId']
        self.summoner_level = self.raw_data['summonerLevel']

    def get_mastery(self, *args):
        url = make_url(*args)
        self.mastery_data = extract_json(url)

    def champion_mastery(self, position, *args):
        self.get_mastery(*args)
        self.champion_id = self.mastery_data[position]['championId']
        self.champion_level = self.mastery_data[position]['championLevel']
        self.champion_points = self.mastery_data[position]['championPoints']
        self.champion_next_level_points = self.mastery_data[position]['championPointsUntilNextLevel']
        self.champion_last_play = self.mastery_data[position]['lastPlayTime']

class champion():

    def __init__(self, identifier):
        if isinstance(identifier, int):
            self.id = identifier
            self.name = champion_id_to_name[identifier]
        else:
            self.name = identifier
            self.id = champion_name_to_id[identifier]

        self.raw_data = extract_json(make_url(data_dragon['unique_champion_json'], self.name, '.json'))
        self.lore = self.raw_data['data'][self.name]['lore']
        self.tags = self.raw_data['data'][self.name]['tags']
        self.partype = self.raw_data['data'][self.name]['partype']
        self.info = self.raw_data['data'][self.name]['info']
        self.stats = self.raw_data['data'][self.name]['stats']
        self.recommended = self.raw_data['data'][self.name]['recommended']

        self.passive = self.raw_data['data'][self.name]['passive']
        self.q = self.raw_data['data'][self.name]['spells'][0]
        self.w = self.raw_data['data'][self.name]['spells'][1]
        self.e = self.raw_data['data'][self.name]['spells'][2]
        self.r = self.raw_data['data'][self.name]['spells'][3]

        self.skin_number = len(self.raw_data['data'][self.name]['skins'])
        self.skins = {}
        for skin in self.raw_data['data'][self.name]['skins']:
            self.skins[skin['name']] = {'id': skin['id'], 'num': skin['num'], 'chromas': skin['chromas']}
        self.skin_names = list(self.skins.keys())

    def get_icons(self):
        self.icon = get_image(make_url(data_dragon['champions_icon'], self.name, '.png'))
        self.passive_icon = get_image(make_url(data_dragon['champion_passive_icon'], self.passive['image']['full']))
        self.q_icon = get_image(make_url(data_dragon['champion_spell_icon'], self.q['image']['full']))
        self.w_icon = get_image(make_url(data_dragon['champion_spell_icon'], self.w['image']['full']))
        self.e_icon = get_image(make_url(data_dragon['champion_spell_icon'], self.e['image']['full']))
        self.r_icon = get_image(make_url(data_dragon['champion_spell_icon'], self.r['image']['full']))

    def download_artwork(self, *args):
        if len(args) == 0:
            skin_index = 0
        else:
            skin_index = self.skins[args[0]]['num']
        self.splash = get_image(make_url(data_dragon['champion_splash'], self.name, '_', str(skin_index), '.jpg'))
        self.banner = get_image(make_url(data_dragon['champions_banner'], self.name, '_', str(skin_index), '.jpg'))

---

player = playerId(head(regions['BR']), query_type['summoner_info'], summoner_name, tail(api_key))

player.champion_mastery(1, head(regions['BR']), query_type['mastery'], player.id, tail(api_key))

main = champion(player.champion_id)

main.get_icons()

main.skin_names

main.download_artwork(main.skin_names[0])

print_img(main.splash)











data_dragon = {
'champions_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json', #JSON all champions
'items_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/item.json', #JSON all items
'summoners_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/summoner.json', #JSON all summoner spells
'profile_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/profileicon.json', #Profile icon image by name

'unique_champion_json':'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion/', #JSON single champion /Qiyana.json

'champion_splash': 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/', #Full champion art (JPG) /Qiyana_0.jpg
'champions_banner': 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/', #Champion banner (JPG) /Qiyana_0.jpg
'champions_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/champion/', #Champion square image (PNG) /Qiyana.png

'champion_passive_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/passive/', #Champion passive image (PNG) /Qiyana_P.png
'champion_spell_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/spell/', #Champion spell image (PNG) /QiyanaR.png

'item_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/', #Item image (PNG) /1001.png

'summoner_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/spell/', #Summoner image (PNG) /SummonerFlash.png

'profile_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/profileicon/' #Profile icon image by id (PNG) /685.png
}
