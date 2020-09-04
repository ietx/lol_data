import urllib.request
import json
import requests

import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO

api_key = 'RGAPI-ede7a593-15a0-41f6-a59d-44cc2c7f7fa9'
region = 'BR'

data_dragon = {
'champions_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json', #JSON all champions
'items_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/item.json', #JSON all items
'summoner_spell_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/summoner.json', #JSON all summoner spells

'unique_champion_json':'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion/', #JSON single champion /Qiyana.json

'champion_passive_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/passive/', #Champion passive image (PNG) /Qiyana_P.png
'champion_spell_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/spell/', #Champion spell image (PNG) /QiyanaR.png

'champion_banner': 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/', #Champion banner (JPG) /Qiyana_0.jpg
'champion_splash': 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/', #Full champion art (JPG) /Qiyana_0.jpg

'champion_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/champion/', #Champion square image (PNG) /Qiyana.png
'item_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/', #Item image (PNG) /1001.png
'summoner_spell_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/spell/', #Summoner image (PNG) /SummonerFlash.png
'profile_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/profileicon/' #Profile icon image by id (PNG) /685.png
}

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
'mastery': 'champion-mastery/v4/champion-masteries/by-summoner/',
'match_history': 'match/v4/matchlists/by-account/',
'match_info': 'match/v4/matches/'
}

def head(region):
    return 'https://' + region + '.api.riotgames.com/lol/'

def tail(api_key):
    return '?api_key=' + api_key

def make_url(*args):
    joined_args = ''
    for arg in args:
        joined_args += str(arg)
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

class Summoner():
    def __init__(self, summoner_name):
        url = make_url(head(regions[region]), query_type['summoner_info'], summoner_name, tail(api_key))
        self.summoner_data = extract_json(url)
        url = make_url(head(regions[region]), query_type['mastery'], self.summoner_data['id'], tail(api_key))
        self.mastery_data = extract_json(url)
        url = make_url(head(regions[region]), query_type['match_history'], self.summoner_data['accountId'], tail(api_key))
        self.match_history_data = extract_json(url)['matches']

    def get_summoner_id(self):
        return self.summoner_data['id']

    def get_account_id(self):
        return self.summoner_data['accountId']

    def get_puu_id(self):
        return self.summoner_data['puuid']

    def get_profile_icon_id(self):
        return self.summoner_data['profileIconId']

    def get_summoner_level(self):
        return self.summoner_data['summonerLevel']

    def get_mastery_data(self, parameter):
        return self.mastery_data[int(parameter)]

    def get_match_data(self, parameter):
        return self.match_history_data[int(parameter)]

    def get_mastery_champion_id(self, parameter):
        return str(self.get_mastery_data(parameter)['championId'])

    def get_match_id(self, parameter):
        return str(self.get_match_history_data(parameter)['gameId'])

class Game():
    def __init__(self, match_id):
        url = make_url(head(regions[region]), query_type['match_info'], str(match_id), tail(api_key))
        self.game_data = extract_json(url)

        for participants in self.game_data['participants']:
            for participant_ids in self.game_data['participantIdentities']:
                if participants['participantId'] == participant_ids['participantId']:
                    participants.update(participant_ids)

        self.game_data.pop('participantIdentities')

    def get_game_id(self):
        return self.game_data['gameId']

    def get_game_creation(self):
        return self.game_data['gameCreation']

    def get_game_duration(self):
        return self.game_data['gameDuration']

    def get_game_season(self):
        return self.game_data['seasonId']

    def get_game_version(self):
        return self.game_data['gameVersion']

    def get_game_mode(self):
        return self.game_data['gameMode']

    def get_game_type(self):
        return self.game_data['gameType']

    def get_team_id(self, side):
        if side == 'blue':
            team_id = 100
        elif side == 'red':
            team_id = 200
        return team_id

    def get_team_info(self, side):
        for team in my_game.game_data['teams']:
            if team['teamId'] == self.get_team_id(side):
                return team

    def get_team_players(self, side):
        players = []
        for participant in self.game_data['participants']:
            if participant['teamId'] == self.get_team_id(side):
                players.append(participant)
        return players

    def get_player_info(self, summoner_name):
        for participant in self.game_data['participants']:
            if participant['player']['summonerName'] == str(summoner_name):
                return participant
                break

    def get_player_spells(self, summoner_name):
        for participant in self.game_data['participants']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'spell_1': participant['spell1Id'],
                'spell_2': participant['spell2Id']
                }
                break

    def get_player_kda(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'kills': participant['kills'],
                'deaths': participant['deaths'],
                'assists': participant['assists']
                }
                break

    def get_player_items(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'item_0': participant['item0'],
                'item_1': participant['item1'],
                'item_2': participant['item2'],
                'item_3': participant['item3'],
                'item_4': participant['item4'],
                'item_5': participant['item5'],
                'item_6': participant['item6']
                }
                break

    def get_player_runes(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'primary_rune': participant['perkPrimaryStyle'],
                'secondary_rune': participant['perkSubStyle'],
                'primary_1': participant['perk0'],
                'primary_2': participant['perk1'],
                'primary_3': participant['perk2'],
                'primary_4': participant['perk3'],
                'secondary_1': participant['perk4'],
                'secondary_2': participant['perk5'],
                'stat_1': participant['statPerk0'],
                'stat_2': participant['statPerk1'],
                'stat_3': participant['statPerk2']
                }
                break

    def get_player_role_lane(self, summoner_name):
        for participant in self.game_data['participants']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'role': participant['timeline']['role'],
                'lane': participant['timeline']['lane']
                }
                break

    def get_player_cs(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'total_cs': participant['totalMinionsKilled'] + participant['neutralMinionsKilled'],
                'jungle_cs': participant['neutralMinionsKilled'],
                'team_jungle_cs': participant['neutralMinionsKilledTeamJungle'],
                'enemy_jungle_cs': participant['neutralMinionsKilledEnemyJungle']
                }
                break

    def get_player_wards(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'vision_score': participant['visionScore'],
                'wards_placed': participant['wardsPlaced'],
                'wards_killed': participant['wardsKilled']
                }
                break

    def get_player_objectives(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'turrets_killed': participant['turretKills'],
                'inhibitors_killed': participant['inhibitorKills']
                }
                break

    def get_player_kills(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'largest_killing_spree': participant['largestKillingSpree'],
                'largest_multi_kill': participant['largestMultiKill'],
                'number_of_killing_sprees': participant['killingSprees']
                }
                break

    def get_player_damage_dealt(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'total': participant['totalDamageDealt'],
                'total_magic': participant['magicDamageDealt'],
                'total_physical': participant['physicalDamageDealt'],
                'total_true': participant['trueDamageDealt'],
                'total_to_champions': participant['totalDamageDealtToChampions'],
                'total_magic_to_champions': participant['magicDamageDealtToChampions'],
                'total_physical_to_champions': participant['physicalDamageDealtToChampions'],
                'total_true_to_champions': participant['trueDamageDealtToChampions'],
                'total_to_objectives': participant['damageDealtToObjectives'],
                'total_to_turrets': participant['damageDealtToTurrets']
                }
                break

    def get_player_damage_received(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'total': participant['totalDamageTaken'],
                'total_magic': participant['magicalDamageTaken'],
                'total_physical': participant['physicalDamageTaken'],
                'total_true': participant['trueDamageTaken']
                }
                break

    def get_player_damage_received(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'total': participant['totalDamageTaken'],
                'total_magic': participant['magicalDamageTaken'],
                'total_physical': participant['physicalDamageTaken'],
                'total_true': participant['trueDamageTaken'],
                'total_self_mitigated': participant['damageSelfMitigated'],
                'total_heal': participant['totalHeal']
                }
                break

    def get_player_cc(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'cc_time_dealt': participant['timeCCingOthers'],
                'cc_time_taken': participant['totalTimeCrowdControlDealt']
                }
                break

    def get_player_gold(self, summoner_name):
        for participant in self.game_data['participants']['stats']:
            if participant['player']['summonerName'] == str(summoner_name):
                return {
                'gold_earned': participant['goldEarned'],
                'gold_spent': participant['goldSpent']
                }
                break

class Champion():
    def __init__(self, identifier):
        url_1 = make_url(data_dragon['champions_json'])
        self.all_champions_data = extract_json(url_1)['data']

        if isinstance(identifier, int):
            self.id = identifier
            for champion_key in self.all_champions_data.keys():
                if int(self.all_champions_data[champion_key]['key']) == identifier:
                    self.name = self.all_champions_data[champion_key]['id']
                    break
        else:
            self.name = identifier
            for champion_key in self.all_champions_data.keys():
                if self.all_champions_data[champion_key]['id'] == identifier:
                    self.id = self.all_champions_data[champion_key]['key']
                    break

        url_2 = make_url(data_dragon['unique_champion_json'], self.name, '.json')
        self.champion_data = extract_json(url_2)['data'][self.name]

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_passive(self):
        return {
        'name': self.champion_data['passive']['name'],
        'description': self.champion_data['passive']['description'],
        'image_id': self.champion_data['passive']['image']['full']
        }
        self.champion_data['passive']

    def get_abilities(self):
        return {
        'q': {
            'id': self.champion_data['spells'][0]['id'],
            'name': self.champion_data['spells'][0]['name'],
            'description': self.champion_data['spells'][0]['description'],
            'maxrank': self.champion_data['spells'][0]['maxrank'],
            'cooldown': self.champion_data['spells'][0]['cooldown'],
            'cost': self.champion_data['spells'][0]['cost'],
            'maxammo': self.champion_data['spells'][0]['maxammo'],
            'range': self.champion_data['spells'][0]['range'],
            'image_id': self.champion_data['spells'][0]['image']['full']
            },
        'w': {
            'id': self.champion_data['spells'][1]['id'],
            'name': self.champion_data['spells'][1]['name'],
            'description': self.champion_data['spells'][1]['description'],
            'maxrank': self.champion_data['spells'][1]['maxrank'],
            'cooldown': self.champion_data['spells'][1]['cooldown'],
            'cost': self.champion_data['spells'][1]['cost'],
            'maxammo': self.champion_data['spells'][1]['maxammo'],
            'range': self.champion_data['spells'][1]['range'],
            'image_id': self.champion_data['spells'][1]['image']['full']
            },
        'e': {
            'id': self.champion_data['spells'][2]['id'],
            'name': self.champion_data['spells'][2]['name'],
            'description': self.champion_data['spells'][2]['description'],
            'maxrank': self.champion_data['spells'][2]['maxrank'],
            'cooldown': self.champion_data['spells'][2]['cooldown'],
            'cost': self.champion_data['spells'][2]['cost'],
            'maxammo': self.champion_data['spells'][2]['maxammo'],
            'range': self.champion_data['spells'][2]['range'],
            'image_id': self.champion_data['spells'][2]['image']['full']
            },
        'r': {
            'id': self.champion_data['spells'][3]['id'],
            'name': self.champion_data['spells'][3]['name'],
            'description': self.champion_data['spells'][3]['description'],
            'maxrank': self.champion_data['spells'][3]['maxrank'],
            'cooldown': self.champion_data['spells'][3]['cooldown'],
            'cost': self.champion_data['spells'][3]['cost'],
            'maxammo': self.champion_data['spells'][3]['maxammo'],
            'range': self.champion_data['spells'][3]['range'],
            'image_id': self.champion_data['spells'][3]['image']['full']
            }
        }

    def get_skins(self):
        skins = {}
        for skin in self.champion_data['skins']:
            skins[skin['id']] = {
                'name': skin['name'],
                'num': skin['num'],
                'chromas': skin['chromas'],
                'image_id': make_url(self.name, '_', str(skin['num']), '.jpg')
                }
        return skins

    def get_lore(self):
        return self.champion_data['lore']

    def get_tags(self):
        return self.champion_data['tags']

    def get_partype(self):
        return self.champion_data['partype']

    def get_info(self):
        return self.champion_data['info']

    def get_stats(self):
        return self.champion_data['stats']

    def get_passive_icon(self):
        return get_image(make_url(data_dragon['champion_passive_icon'], self.get_passive()['image']))

    def get_ability_icon(self, ability):
        return get_image(make_url(data_dragon['champion_spell_icon'], self.get_abilities()[ability]['image_id']))

    def get_icon(self):
        return get_image(make_url(data_dragon['champion_icon'], self.champion_data['image']['full']))

    def get_splash(self, *args):
        if len(args) == 0:
            image_id = self.get_skins()[str(self.id) + '000']['image_id']
        else:
            image_id = self.get_skins()[str(args[0])]['image_id']
        return get_image(make_url(data_dragon['champion_splash'], image_id))

    def get_banner(self, *args):
        if len(args) == 0:
            image_id = self.get_skins()[str(self.id) + '000']['image_id']
        else:
            image_id = self.get_skins()[str(args[0])]['image_id']
        return get_image(make_url(data_dragon['champion_banner'], image_id))

class Item():
    def __init__(self, identifier):
        url = make_url(data_dragon['items_json'])
        self.all_items_data = extract_json(url)['data']

        if isinstance(identifier, int):
            self.id = identifier
            for item_key in self.all_items_data.keys():
                if int(item_key) == identifier:
                    self.name = self.all_items_data[item_key]['name']
                    break
        else:
            self.name = identifier
            for item_key in self.all_items_data.keys():
                if self.all_items_data[item_key]['name'] == identifier:
                    self.id = int(item_key)
                    break

        self.item_data = self.all_items_data[str(self.id)]

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_description(self):
        return self.item_data['plaintext']

    def get_tags(self):
        return self.item_data['tags']

    def get_stats(self):
        return self.item_data['stats']

    def get_prices(self):
        return {
        'buy': self.item_data['gold']['total'],
        'sell': self.item_data['gold']['sell']
        }

    def get_image_id(self):
        return self.item_data['image']['full']

    def get_image(self):
        return get_image(make_url(data_dragon['item_icon'], self.get_image_id()))

class SummonerSpell():
    def __init__(self, identifier):
        url = make_url(data_dragon['summoner_spell_json'])
        self.all_summoner_spell_data = extract_json(url)['data']

        if isinstance(identifier, int):
            self.id = identifier
            for summoner_spell_key in self.all_summoner_spell_data.keys():
                if int(self.all_summoner_spell_data[summoner_spell_key]['key']) == identifier:
                    self.name = self.all_summoner_spell_data[summoner_spell_key]['name']
                    self.summoner_key = summoner_spell_key
                    break
        else:
            self.name = identifier
            for summoner_spell_key in self.all_summoner_spell_data.keys():
                if self.all_summoner_spell_data[summoner_spell_key]['name'] == identifier:
                    self.id = int(summoner_spell_key)
                    self.summoner_key = summoner_spell_key
                    break

        self.summoner_spell_data = self.all_summoner_spell_data[self.summoner_key]

    def get_description(self):
        return self.summoner_spell_data['description']

    def get_cooldown(self):
        return self.summoner_spell_data['cooldown']

    def get_efect(self):
        return self.summoner_spell_data['effect']

    def get_range(self):
        return self.summoner_spell_data['range']

    def get_image_id(self):
        return self.summoner_spell_data['image']['full']

    def get_image(self):
        return get_image(make_url(data_dragon['summoner_spell_icon'], self.get_image_id()))

###

my_game = Game(2048253838)
my_game.get_player_info('ietx')

Qiqi = Champion('Qiyana')
Qiqi.id
Qiqi.get_banner()

items_data = extract_json(data_dragon['items_json'])
items_data['data']

item = Item('Boots of Speed')
item.get_image()

barrier = SummonerSpell(21)
barrier.get_image()
