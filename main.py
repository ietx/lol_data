import urllib.request
import json
import requests

import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO

data_dragon = {
'champions_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json', #JSON all champions
'items_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/item.json', #JSON all items
'summoners_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/summoner.json', #JSON all summoner spells
'profile_json': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/profileicon.json', #Profile icon image by name

'unique_champion_json':'http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion/', #JSON single champion /Qiyana.json

'champion_splash': 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/', #Full champion art (JPG) /Qiyana_0.jpg
'champion_banner': 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/', #Champion banner (JPG) /Qiyana_0.jpg
'champion_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/champion/', #Champion square image (PNG) /Qiyana.png

'champion_passive_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/passive/', #Champion passive image (PNG) /Qiyana_P.png
'champion_spell_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/spell/', #Champion spell image (PNG) /QiyanaR.png

'item_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/', #Item image (PNG) /1001.png

'summoner_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/spell/', #Summoner image (PNG) /SummonerFlash.png

'profile_icon': 'http://ddragon.leagueoflegends.com/cdn/10.16.1/img/profileicon/' #Profile icon image by id (PNG) /685.png
}

api_key = 'RGAPI-4dd1dc72-57c0-4feb-b2b5-26052b96cb59'

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
'mastery': 'champion-mastery/v4/champion-masteries/by-summoner/',
'match_history': 'match/v4/matchlists/by-account/',
'match_info': 'match/v4/matches/',
'match_timeline': 'match/v4/timelines/by-match/'
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

champions_data = extract_json(data_dragon['champions_json'])
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
        self.raw_data = extract_json(url)
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

    def get_match_history(self, *args):
        url = make_url(*args)
        self.raw_match_history_data = extract_json(url)['matches']

class champion():

    def __init__(self, identifier):
        if isinstance(identifier, int):
            self.id = identifier
            self.name = champion_id_to_name[identifier]
        else:
            self.name = identifier
            self.id = champion_name_to_id[identifier]

        url = make_url(data_dragon['unique_champion_json'], self.name, '.json')
        self.raw_data = extract_json(url)
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

    def get_icon(self):
        self.icon = get_image(make_url(data_dragon['champion_icon'], self.name, '.png'))

    def get_ability_icons(self):
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
        self.banner = get_image(make_url(data_dragon['champion_banner'], self.name, '_', str(skin_index), '.jpg'))

###

player = playerId(head(regions['BR']), query_type['summoner_info'], summoner_name, tail(api_key))

player.champion_mastery(1, head(regions['BR']), query_type['mastery'], player.id, tail(api_key))

main = champion(player.champion_id)

main.get_icons()

main.skin_names

main.download_artwork(main.skin_names[0])

print_img(main.splash)

make_url(head(regions['BR']), query_type['match_history'], player.account_id, tail(api_key))

extract_json(make_url(head(regions['BR']), query_type['match_history'], player.account_id, tail(api_key)))['matches']


'https://br1.api.riotgames.com/lol/match/v4/matches/2014009757?api_key=RGAPI-f04af0c5-dae9-4686-ab07-e0af39954ef5'
'https://br1.api.riotgames.com/lol/match/v4/timelines/by-match/2044890620?api_key=RGAPI-f04af0c5-dae9-4686-ab07-e0af39954ef5'
2048432107



extract_json(make_url(head(regions['BR']), query_type['match_info'], '2048377021', tail(api_key)))['participants'][0]['stats']

class game():

    def __init__(self, *args):
        url = make_url(*args)
        self.raw_gaming_data = extract_json(url)
        self.game_id = self.raw_gaming_data['gameId']
        self.creation = self.raw_gaming_data['gameCreation']
        self.duration = self.raw_gaming_data['gameDuration']
        self.season = self.raw_gaming_data['seasonId']
        self.version = self.raw_gaming_data['gameVersion']
        self.mode = self.raw_gaming_data['gameMode']
        self.type = self.raw_gaming_data['gameType']

class team(game):

    def __init__(self, side, *args):
        super(team, self).__init__(*args)
        if side == 'blue':
            index = 0
        elif side == 'red':
            index = 1
        self.team_id = self.raw_gaming_data['teams'][index]['teamId']
        self.first_blood = self.raw_gaming_data['teams'][index]['firstBlood']
        self.first_tower = self.raw_gaming_data['teams'][index]['firstTower']
        self.first_inhibitor = self.raw_gaming_data['teams'][index]['firstInhibitor']
        self.first_baron = self.raw_gaming_data['teams'][index]['firstBaron']
        self.first_dragon = self.raw_gaming_data['teams'][index]['firstDragon']
        self.first_rift_herald = self.raw_gaming_data['teams'][index]['firstRiftHerald']
        self.tower_kills = self.raw_gaming_data['teams'][index]['towerKills']
        self.inhibitor_kills = self.raw_gaming_data['teams'][index]['inhibitorKills']
        self.baron_bills = self.raw_gaming_data['teams'][index]['baronKills']
        self.dragon_kills = self.raw_gaming_data['teams'][index]['dragonKills']
        self.vilemaw_kills = self.raw_gaming_data['teams'][index]['vilemawKills']
        self.rift_herald_kills = self.raw_gaming_data['teams'][index]['riftHeraldKills']

        self.bans = self.raw_gaming_data['teams'][0]['bans']
        try:
            self.ban_ids = []
            for ban in self.bans:
                self.ban_ids.append(ban['championId'])
        except:
            pass

    def get_players(self, *args):
        self.players_list = []

        for i, player in enumerate(self.raw_gaming_data['participantIdentities']):
            if self.raw_gaming_data['participants'][i]['teamId'] != self.team_id:
                pass
            else:
                player_dict = {}
                player_dict['participant_id'] = player['participantId']
                player_dict['account_id'] = player['player']['accountId']
                player_dict['summoner_name'] = player['player']['summonerName']
                player_dict['summoner_id'] = player['player']['summonerId']
                player_dict['profile_icon'] = player['player']['profileIcon']
                player_dict['team_id'] = self.raw_gaming_data['participants'][i]['teamId']
                player_dict['champion_id'] = self.raw_gaming_data['participants'][i]['championId']
                player_dict['summoner_spell_1_id'] = self.raw_gaming_data['participants'][i]['spell1Id']
                player_dict['summoner_spell_2_id'] = self.raw_gaming_data['participants'][i]['spell2Id']
                player_dict['result'] = self.raw_gaming_data['participants'][i]['stats']['win']
                player_dict['item_0_id'] = self.raw_gaming_data['participants'][i]['stats']['item0']
                player_dict['item_1_id'] = self.raw_gaming_data['participants'][i]['stats']['item1']
                player_dict['item_2_id'] = self.raw_gaming_data['participants'][i]['stats']['item2']
                player_dict['item_3_id'] = self.raw_gaming_data['participants'][i]['stats']['item3']
                player_dict['item_4_id'] = self.raw_gaming_data['participants'][i]['stats']['item4']
                player_dict['item_5_id'] = self.raw_gaming_data['participants'][i]['stats']['item5']
                player_dict['item_6_id'] = self.raw_gaming_data['participants'][i]['stats']['item6']
                player_dict['level'] = self.raw_gaming_data['participants'][i]['stats']['champLevel']
                player_dict['kills'] = self.raw_gaming_data['participants'][i]['stats']['kills']
                player_dict['deaths'] = self.raw_gaming_data['participants'][i]['stats']['deaths']
                player_dict['assists'] = self.raw_gaming_data['participants'][i]['stats']['assists']
                player_dict['largest_killing_spree'] = self.raw_gaming_data['participants'][i]['stats']['largestKillingSpree']
                player_dict['largest_multi_kill'] = self.raw_gaming_data['participants'][i]['stats']['largestMultiKill']
                player_dict['longest_time_living'] = self.raw_gaming_data['participants'][i]['stats']['longestTimeSpentLiving']
                player_dict['total_damage_dealt'] = self.raw_gaming_data['participants'][i]['stats']['totalDamageDealt']
                player_dict['magic_damage_dealt'] = self.raw_gaming_data['participants'][i]['stats']['magicDamageDealt']
                player_dict['physical_damage_dealt'] = self.raw_gaming_data['participants'][i]['stats']['physicalDamageDealt']
                player_dict['true_damage_dealt'] = self.raw_gaming_data['participants'][i]['stats']['trueDamageDealt']
                player_dict['total_damage_dealt_to_champions'] = self.raw_gaming_data['participants'][i]['stats']['totalDamageDealtToChampions']
                player_dict['magic_damage_dealt_to_champions'] = self.raw_gaming_data['participants'][i]['stats']['magicDamageDealtToChampions']
                player_dict['physical_damage_dealt_to_champions'] = self.raw_gaming_data['participants'][i]['stats']['physicalDamageDealtToChampions']
                player_dict['true_damage_dealt_to_champions'] = self.raw_gaming_data['participants'][i]['stats']['trueDamageDealtToChampions']
                player_dict['total_damage_dealt_to_objectives'] = self.raw_gaming_data['participants'][i]['stats']['damageDealtToObjectives']
                player_dict['total_damage_dealt_to_turrets'] = self.raw_gaming_data['participants'][i]['stats']['damageDealtToTurrets']
                player_dict['total_damage_self_mitigated'] = self.raw_gaming_data['participants'][i]['stats']['damageSelfMitigated']
                player_dict['total_heal'] = self.raw_gaming_data['participants'][i]['stats']['totalHeal']
                player_dict['vision_score'] = self.raw_gaming_data['participants'][i]['stats']['visionScore']
                player_dict['time_ccing_others'] = self.raw_gaming_data['participants'][i]['stats']['timeCCingOthers']
                player_dict['total_damage_taken'] = self.raw_gaming_data['participants'][i]['stats']['totalDamageTaken']
                player_dict['magical_damage_taken'] = self.raw_gaming_data['participants'][i]['stats']['magicalDamageTaken']
                player_dict['physical_damage_taken'] = self.raw_gaming_data['participants'][i]['stats']['physicalDamageTaken']
                player_dict['true_damage_taken'] = self.raw_gaming_data['participants'][i]['stats']['trueDamageTaken']
                player_dict['gold_earned'] = self.raw_gaming_data['participants'][i]['stats']['goldEarned']
                player_dict['gold_spent'] = self.raw_gaming_data['participants'][i]['stats']['goldSpent']
                player_dict['turret_kills'] = self.raw_gaming_data['participants'][i]['stats']['turretKills']
                player_dict['inhibitor_kills'] = self.raw_gaming_data['participants'][i]['stats']['inhibitorKills']
                player_dict['cs_score'] = self.raw_gaming_data['participants'][i]['stats']['totalMinionsKilled'] + self.raw_gaming_data['participants'][i]['stats']['neutralMinionsKilled']
                player_dict['minions_killed_team_jungle'] = self.raw_gaming_data['participants'][i]['stats']['neutralMinionsKilledTeamJungle']
                player_dict['minions_killed_enemy_jungle'] = self.raw_gaming_data['participants'][i]['stats']['neutralMinionsKilledEnemyJungle']
                player_dict['total_time_ccing_dealt'] = self.raw_gaming_data['participants'][i]['stats']['totalTimeCrowdControlDealt']
                player_dict['wards_placed'] = self.raw_gaming_data['participants'][i]['stats']['wardsPlaced']
                player_dict['wards_killed'] = self.raw_gaming_data['participants'][i]['stats']['wardsKilled']
                player_dict['first_blood_kill'] = self.raw_gaming_data['participants'][i]['stats']['firstBloodKill']
                player_dict['first_blood_assist'] = self.raw_gaming_data['participants'][i]['stats']['firstBloodAssist']
                player_dict['first_tower_kill'] = self.raw_gaming_data['participants'][i]['stats']['firstTowerKill']
                player_dict['first_tower_assist'] = self.raw_gaming_data['participants'][i]['stats']['firstTowerAssist']
                player_dict['creeps_per_min_deltas'] = self.raw_gaming_data['participants'][i]['timeline']['creepsPerMinDeltas']
                player_dict['xp_per_min_deltas'] = self.raw_gaming_data['participants'][i]['timeline']['xpPerMinDeltas']
                player_dict['gold_per_min_deltas'] = self.raw_gaming_data['participants'][i]['timeline']['goldPerMinDeltas']
                player_dict['lane'] = self.raw_gaming_data['participants'][i]['timeline']['lane']
                self.players_list.append(player_dict)
                if len(args) == 0:
                    pass
                else:
                    if player_dict['summoner_name'] == args[0]:
                        self.summoner_info = player_dict

a = team('red', head(regions['BR']), query_type['match_info'], '2048377021', tail(api_key))

a.get_players('ietx')
a.players_list[1]['kills']
a.summoner_info['result']
