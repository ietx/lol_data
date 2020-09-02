import urllib.request
import json
import requests

import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO

api_key = 'RGAPI-4bae7798-aec1-482b-8511-1f10448d5fe3'
summoner_name = 'ietx'
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

def get_icon(type, info):
    if type == 'champion_icon':
        return get_image(make_url(data_dragon[type], info, '.png'))
    elif type == 'item_icon':
        return get_image(make_url(data_dragon[type], info, '.png'))
    elif type == 'summoner_icon':
        return get_image(make_url(data_dragon[type], info, '.png'))
    elif type == 'profile_icon':
        return get_image(make_url(data_dragon[type], info, '.png'))

champions_data = extract_json(data_dragon['champions_json'])
def champion_id_name(champions_data):
    champion_names = list(champions_data['data'].keys())
    champion_name_to_id = {}
    for name in champion_names:
        champion_name_to_id[name] = int(champions_data['data'][name]['key'])
    champion_id_to_name = {v: k for (k, v) in champion_name_to_id.items()}
    return champion_name_to_id, champion_id_to_name
champion_name_to_id, champion_id_to_name = champion_id_name(champions_data)

items_data = extract_json(data_dragon['items_json'])
def item_id_name(champions_data):
    item_ids = list(champions_data['data'].keys())
    items_id_to_name = {}
    for item in item_ids:
        items_id_to_name[item] = items_data['data'][item]['name']
    items_name_to_id = {v: k for (k, v) in items_id_to_name.items()}
    return items_id_to_name, items_name_to_id
items_id_to_name, items_name_to_id = item_id_name(items_data)

summoner_spell_data = extract_json(data_dragon['summoner_spell_json'])
def summoner_spell_id_name(champions_data):
    summoner_spell_ids = list(summoner_spell_data['data'].keys())
    summoner_spell_id_to_name = {}
    for summoner_spell in summoner_spell_ids:
        summoner_spell_id_to_name[summoner_spell] = summoner_spell_data['data'][summoner_spell]['name']
    summoner_spell_name_to_id = {v: k for (k, v) in summoner_spell_id_to_name.items()}
    return summoner_spell_id_to_name, summoner_spell_name_to_id
summoner_spell_id_to_name, summoner_spell_name_to_id = summoner_spell_id_name(items_data)

class Summoner():
    def __init__(self, summoner_name):
        url = make_url(head(regions[region]), query_type['summoner_info'], summoner_name, tail(api_key))
        self.summoner_data = extract_json(url)
        self.summoner_id = self.summoner_data['id']
        self.account_id = self.summoner_data['accountId']
        self.puu_id = self.summoner_data['puuid']
        self.name = self.summoner_data['name']
        self.profile_icon_id = self.summoner_data['profileIconId']
        self.summoner_level = self.summoner_data['summonerLevel']

    def get_mastery(self):
        url = make_url(head(regions[region]), query_type['mastery'], self.summoner_id, tail(api_key))
        self.mastery_data = extract_json(url)

    def champion_mastery(self, position):
        self.get_mastery()
        self.champion_id = self.mastery_data[position]['championId']
        self.champion_level = self.mastery_data[position]['championLevel']
        self.champion_points = self.mastery_data[position]['championPoints']
        self.champion_next_level_points = self.mastery_data[position]['championPointsUntilNextLevel']
        self.champion_last_play = self.mastery_data[position]['lastPlayTime']

    def get_match_history(self):
        url = make_url(head(regions[region]), query_type['match_history'], self.account_id, tail(api_key))
        self.match_history_data = extract_json(url)['matches']

    def get_match(self, position):
        self.get_match_history()
        self.match_id = self.match_history_data[position]['gameId']
        self.match_timestamp = self.match_history_data[position]['timestamp']
        self.match_champion_id = self.match_history_data[position]['champion']

class Game():
    def __init__(self, match_id):
        url = make_url(head(regions[region]), query_type['match_info'], match_id, tail(api_key))
        self.game_data = extract_json(url)
        self.game_id = self.game_data['gameId']
        self.creation = self.game_data['gameCreation']
        self.duration = self.game_data['gameDuration']
        self.season = self.game_data['seasonId']
        self.version = self.game_data['gameVersion']
        self.mode = self.game_data['gameMode']
        self.type = self.game_data['gameType']

class gameSummoner(Game):
    def __init__(self, match_id):
        super(gameSummoner, self).__init__(match_id)

    def get_player_info(self, player):
        player_dict = {}
        player_dict['participant_id'] = player['participantId']
        player_dict['account_id'] = player['player']['accountId']
        player_dict['summoner_name'] = player['player']['summonerName']
        player_dict['summoner_id'] = player['player']['summonerId']
        player_dict['profile_icon'] = player['player']['profileIcon']
        for participant in self.game_data['participants']:
            if participant['participantId'] == player_dict['participant_id']:
                player_dict['team_id'] = participant['teamId']
                player_dict['champion_id'] = participant['championId']
                player_dict['summoner_spell_1_id'] = participant['spell1Id']
                player_dict['summoner_spell_2_id'] = participant['spell2Id']
                player_dict['result'] = participant['stats']['win']
                player_dict['item_0_id'] = participant['stats']['item0']
                player_dict['item_1_id'] = participant['stats']['item1']
                player_dict['item_2_id'] = participant['stats']['item2']
                player_dict['item_3_id'] = participant['stats']['item3']
                player_dict['item_4_id'] = participant['stats']['item4']
                player_dict['item_5_id'] = participant['stats']['item5']
                player_dict['item_6_id'] = participant['stats']['item6']
                player_dict['level'] = participant['stats']['champLevel']
                player_dict['kills'] = participant['stats']['kills']
                player_dict['deaths'] = participant['stats']['deaths']
                player_dict['assists'] = participant['stats']['assists']
                player_dict['largest_killing_spree'] = participant['stats']['largestKillingSpree']
                player_dict['largest_multi_kill'] = participant['stats']['largestMultiKill']
                player_dict['longest_time_living'] = participant['stats']['longestTimeSpentLiving']
                player_dict['total_damage_dealt'] = participant['stats']['totalDamageDealt']
                player_dict['magic_damage_dealt'] = participant['stats']['magicDamageDealt']
                player_dict['physical_damage_dealt'] = participant['stats']['physicalDamageDealt']
                player_dict['true_damage_dealt'] = participant['stats']['trueDamageDealt']
                player_dict['total_damage_dealt_to_champions'] = participant['stats']['totalDamageDealtToChampions']
                player_dict['magic_damage_dealt_to_champions'] = participant['stats']['magicDamageDealtToChampions']
                player_dict['physical_damage_dealt_to_champions'] = participant['stats']['physicalDamageDealtToChampions']
                player_dict['true_damage_dealt_to_champions'] = participant['stats']['trueDamageDealtToChampions']
                player_dict['total_damage_dealt_to_objectives'] = participant['stats']['damageDealtToObjectives']
                player_dict['total_damage_dealt_to_turrets'] = participant['stats']['damageDealtToTurrets']
                player_dict['total_damage_self_mitigated'] = participant['stats']['damageSelfMitigated']
                player_dict['total_heal'] = participant['stats']['totalHeal']
                player_dict['vision_score'] = participant['stats']['visionScore']
                player_dict['time_ccing_others'] = participant['stats']['timeCCingOthers']
                player_dict['total_damage_taken'] = participant['stats']['totalDamageTaken']
                player_dict['magical_damage_taken'] = participant['stats']['magicalDamageTaken']
                player_dict['physical_damage_taken'] = participant['stats']['physicalDamageTaken']
                player_dict['true_damage_taken'] = participant['stats']['trueDamageTaken']
                player_dict['gold_earned'] = participant['stats']['goldEarned']
                player_dict['gold_spent'] = participant['stats']['goldSpent']
                player_dict['turret_kills'] = participant['stats']['turretKills']
                player_dict['inhibitor_kills'] = participant['stats']['inhibitorKills']
                player_dict['cs_score'] = participant['stats']['totalMinionsKilled'] + participant['stats']['neutralMinionsKilled']
                player_dict['minions_killed_team_jungle'] = participant['stats']['neutralMinionsKilledTeamJungle']
                player_dict['minions_killed_enemy_jungle'] = participant['stats']['neutralMinionsKilledEnemyJungle']
                player_dict['total_time_ccing_dealt'] = participant['stats']['totalTimeCrowdControlDealt']
                player_dict['wards_placed'] = participant['stats']['wardsPlaced']
                player_dict['wards_killed'] = participant['stats']['wardsKilled']
                try:
                    player_dict['first_blood_kill'] = participant['stats']['firstBloodKill']
                    player_dict['first_blood_assist'] = participant['stats']['firstBloodAssist']
                    player_dict['first_tower_kill'] = participant['stats']['firstTowerKill']
                    player_dict['first_tower_assist'] = participant['stats']['firstTowerAssist']
                except:
                    pass
                player_dict['primary_rune'] = participant['stats']['perkPrimaryStyle']
                player_dict['secondary_rune'] = participant['stats']['perkSubStyle']
                player_dict['primary_rune_1'] = participant['stats']['perk0']
                player_dict['primary_rune_2'] = participant['stats']['perk1']
                player_dict['primary_rune_3'] = participant['stats']['perk2']
                player_dict['primary_rune_4'] = participant['stats']['perk3']
                player_dict['secondary_rune_1'] = participant['stats']['perk4']
                player_dict['secondary_rune_2'] = participant['stats']['perk5']
                try:
                    player_dict['creeps_per_min_deltas'] = participant['timeline']['creepsPerMinDeltas']
                    player_dict['xp_per_min_deltas'] = participant['timeline']['xpPerMinDeltas']
                    player_dict['gold_per_min_deltas'] = participant['timeline']['goldPerMinDeltas']
                except:
                    pass
                player_dict['role'] = participant['timeline']['role']
                player_dict['lane'] = participant['timeline']['lane']
        return player_dict

    def get_summoner_info(self, summoner_name):
        for player in self.game_data['participantIdentities']:
            if player['player']['summonerName'] == summoner_name:
                self.summoner_info = self.get_player_info(player)

class gameTeam(gameSummoner):

    def __init__(self, side, match_id):
        super(gameTeam, self).__init__(match_id)

        if side == 'blue':
            index = 0
        elif side == 'red':
            index = 1

        self.team_id = self.game_data['teams'][index]['teamId']
        self.first_blood = self.game_data['teams'][index]['firstBlood']
        self.first_tower = self.game_data['teams'][index]['firstTower']
        self.first_inhibitor = self.game_data['teams'][index]['firstInhibitor']
        self.first_baron = self.game_data['teams'][index]['firstBaron']
        self.first_dragon = self.game_data['teams'][index]['firstDragon']
        self.first_rift_herald = self.game_data['teams'][index]['firstRiftHerald']
        self.tower_kills = self.game_data['teams'][index]['towerKills']
        self.inhibitor_kills = self.game_data['teams'][index]['inhibitorKills']
        self.baron_bills = self.game_data['teams'][index]['baronKills']
        self.dragon_kills = self.game_data['teams'][index]['dragonKills']
        self.vilemaw_kills = self.game_data['teams'][index]['vilemawKills']
        self.rift_herald_kills = self.game_data['teams'][index]['riftHeraldKills']

        self.bans = self.game_data['teams'][index]['bans']
        try:
            self.ban_ids = []
            for ban in self.bans:
                self.ban_ids.append(ban['championId'])
        except:
            pass

    def get_players_info(self):
        self.players_list = []
        for player in self.game_data['participantIdentities']:
            for participant in self.game_data['participants']:
                if participant['participantId'] == player['participantId']:
                    if participant['teamId'] == self.team_id:
                        self.players_list.append(self.get_player_info(player))

class Champion():
    def __init__(self, identifier):
        if isinstance(identifier, int):
            self.id = identifier
            self.name = champion_id_to_name[identifier]
        else:
            self.name = identifier
            self.id = champion_name_to_id[identifier]

        url = make_url(data_dragon['unique_champion_json'], self.name, '.json')
        self.champion_data = extract_json(url)
        self.lore = self.champion_data['data'][self.name]['lore']
        self.tags = self.champion_data['data'][self.name]['tags']
        self.partype = self.champion_data['data'][self.name]['partype']
        self.info = self.champion_data['data'][self.name]['info']
        self.stats = self.champion_data['data'][self.name]['stats']
        self.recommended = self.champion_data['data'][self.name]['recommended']

        self.passive = self.champion_data['data'][self.name]['passive']
        self.q = self.champion_data['data'][self.name]['spells'][0]
        self.w = self.champion_data['data'][self.name]['spells'][1]
        self.e = self.champion_data['data'][self.name]['spells'][2]
        self.r = self.champion_data['data'][self.name]['spells'][3]

        self.skin_number = len(self.champion_data['data'][self.name]['skins'])
        self.skins = {}
        for skin in self.champion_data['data'][self.name]['skins']:
            self.skins[skin['name']] = {'id': skin['id'], 'num': skin['num'], 'chromas': skin['chromas']}
        self.skin_names = list(self.skins.keys())

        self.icon = get_image(make_url(data_dragon['champion_icon'], self.name, '.png'))

    def get_ability_icons(self):
        self.passive_icon = get_image(make_url(data_dragon['champion_passive_icon'], self.passive['image']['full']))
        self.q_icon = get_image(make_url(data_dragon['champion_spell_icon'], self.q['image']['full']))
        self.w_icon = get_image(make_url(data_dragon['champion_spell_icon'], self.w['image']['full']))
        self.e_icon = get_image(make_url(data_dragon['champion_spell_icon'], self.e['image']['full']))
        self.r_icon = get_image(make_url(data_dragon['champion_spell_icon'], self.r['image']['full']))

    def get_artwork(self, *args):
        if len(args) == 0:
            skin_index = 0
        else:
            skin_index = self.skins[args[0]]['num']
        self.splash = get_image(make_url(data_dragon['champion_splash'], self.name, '_', str(skin_index), '.jpg'))
        self.banner = get_image(make_url(data_dragon['champion_banner'], self.name, '_', str(skin_index), '.jpg'))

###

player = Summoner(summoner_name)
player.champion_mastery(1)
player.get_match(6)
player.profile_icon_id

champ = Champion(69)
print_img(champ.icon)
champ.get_ability_icons()
champ.skin_names
champ.get_artwork(champ.skin_names[3])
print_img(champ.splash)

game = gameSummoner(player.match_id)
game.get_summoner_info(summoner_name)
game.summoner_info


game_blue = gameTeam('blue', player.match_id)
game_blue.get_players_info()
game_blue.players_list[0]

leblanc = Champion('Cassiopeia')
leblanc.skins
