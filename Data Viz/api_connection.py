from difflib import get_close_matches
import pandas as pd
from mobfot import MobFot
from difflib import get_close_matches
client  = MobFot()

def add_subs(match, homePlayers, awayPlayers):
    for index_team, team in enumerate(match['content']['lineup']['bench']['benchArr']):
        for player in team:
            if player['minutesPlayed'] > 0:
                if index_team == 0:
                    homePlayers.append(player)
                else:
                    awayPlayers.append(player)
                
    
def get_player_data(match):
    homePlayers = list()
    for x in match['content']['lineup']['lineup'][0]['players']:
        for y in x:
            homePlayers.append(y)

    awayPlayers = list()
    for x in match['content']['lineup']['lineup'][1]['players']:
        for y in x:
            awayPlayers.append(y)
    
    add_subs(match, homePlayers, awayPlayers)  
    return homePlayers, awayPlayers

def parse_api_results(player):
    if not player['isGoalkeeper']:
        name = player['name']['fullName']
        if 'positionStringShort' not in player.keys():
            position = 'substitute'
        else:
            position = player['positionStringShort']
        rating  = player['rating']['num']
        shotmap = player['shotmap']
        role = player['role'].lower()
        stats = player['stats']
        shotmaps = []
        for y in shotmap:
            current_shotmap = {}
            current_shotmap['eventType'] = y['eventType']
            current_shotmap['isOnTarget'] = y['isOnTarget']
            current_shotmap['min'] = y['min']
            current_shotmap['situation'] = y['situation']
            current_shotmap['x'] = y['x']
            current_shotmap['y'] = y['y']
            current_shotmap['goalCrossedY'] = y['goalCrossedY']
            current_shotmap['goalCrossedZ'] = y['goalCrossedZ']
            shotmaps.append(current_shotmap)
        
        
        
        for x in stats:
            if x['key'] == 'top_stats':
                top_stats = x
                new_top_stats = dict()
                for y in top_stats['stats']:
                    new_top_stats[top_stats['stats'][y]['key']] = top_stats['stats'][y]['value']
                top_stats = new_top_stats
            elif x['key'] == 'attack':
                attack_stats = x
                new_attack_stats = dict()
                for y in attack_stats['stats']:
                    new_attack_stats[attack_stats['stats'][y]['key']] = attack_stats['stats'][y]['value']
                attack_stats = new_attack_stats
            elif x['key'] == 'defense':
                defense_stats = x
                new_defense_stats = dict()
                for y in defense_stats['stats']:
                    new_defense_stats[defense_stats['stats'][y]['key']] = defense_stats['stats'][y]['value']
                defense_stats = new_defense_stats
            elif x['key'] == 'duels':
                duel_stats = x
                new_duel_stats = dict()
                for y in duel_stats['stats']:
                    new_duel_stats[duel_stats['stats'][y]['key']] = duel_stats['stats'][y]['value']
                duel_stats = new_duel_stats
        
        new_results = {
        'name': name,
        'position': position,
        'rating': rating,
        'role': role,
        'top_stats': top_stats,
        'attack_stats': attack_stats,
        'defense_stats': defense_stats,
        'duel_stats': duel_stats,
        'shotmaps': shotmaps
    }
    else:
        name = player['name']['fullName']
        if 'positionStringShort' not in player.keys():
            position = 'substitute'
        else:
            position = player['positionStringShort']
        
        rating  = player['rating']['num']
        role = player['role'].lower()
        top_stats = player['stats'][0]  
        new_results = {
        'name': name,
        'position': position,
        'rating': rating,
        'role': role,
        'top_stats': top_stats
    }
    
    
    return new_results
    