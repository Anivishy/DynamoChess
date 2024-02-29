import requests
import json
from pprint import pprint
import time
import io, base64
import os

lichess_key = 'lip_C5pUNarDHGmLKHnTcvus'
seed_name = 'drnykterstein'
following_url = 'https://lichess.org/api/rel/following'

def update_games_url (name):
    return 'https://lichess.org/api/games/user/' + str(name)

# Keys are strings of the repsective game ranges ie. '1000 - 1399'
# Contains a List of Lists, format of each nested list: [game id, game elo, moves, whiteplayerid, blackplayerid]
games = {'1000-1399': [[]],
         '1400-1799': [[]],
         '1800-2199': [[]],
         '2200-2599': [[]],
         '2600-2999': [[]],
         '3000-3399': [[]],
         '3400-3799': [[]],
         '3800-4199': [[]]
         }

unchecked_users = []
users_database = []
game_ids = []
unchecked_users.append(seed_name)

def get_games(seed_user):
    seed_games = requests.get(update_games_url(seed_user),
                params = {
                    'max': 1000
                },
                headers = {
                    'Authorization': f'Bearer {lichess_key}',
                    'Accept': 'application/x-ndjson'
                }                         
    )

    games_json = []

    ndjson = seed_games.content.decode().split('\n')

    for json_obj in ndjson:
        if json_obj:
            games_json.append(json.loads(json_obj))

    return games_json

for user in unchecked_users:
    user_games = get_games(user)
    users_database.append(user)
    unchecked_users.remove(user)
    for game in user_games:
        try:
            if game['id'] in game_ids or game['source'] == 'ai':
                pass
            else:
                pprint(game)
                black = game['players']['black']
                white = game['players']['white']
                game_id = game['id']
                game_ids.append(game_id)
                game_rating = (black['rating'] + white['rating']) // 2
                victory_status = game['status']
                winner = game['winner']
                if game_rating >= 1000:
                    if white['user']['id'] == user:
                        if black['user']['id'] not in unchecked_users:
                            unchecked_users.append(black['user']['id'])
                        else:
                            pass
                    else:
                        if white['user']['id'] not in unchecked_users:
                            unchecked_users.append(white['user']['id'])

                    if game_rating > 1000 and game_rating < 1399:
                        games['1000-1399'].append([game_id, game_rating, game['moves'], white, black, victory_status, winner])

                    elif game_rating > 1400 and game_rating < 1799:
                        games['1400-1799'].append([game_id, game_rating, game['moves'], white, black, victory_status, winner])

                    elif game_rating > 1800 and game_rating < 2199:
                        games['1800-2199'].append([game_id, game_rating, game['moves'], white, black, victory_status, winner])

                    elif game_rating > 2200 and game_rating < 2599:
                        games['2200-2599'].append([game_id, game_rating, game['moves'], white, black, victory_status, winner])

                    elif game_rating > 2600 and game_rating < 2999:
                        games['2600-2999'].append([game_id, game_rating, game['moves'], white, black, victory_status, winner])

                    elif game_rating > 3000 and game_rating < 3399:
                        games['3000-3399'].append([game_id, game_rating, game['moves'], white, black, victory_status, winner])

                    elif game_rating > 3400 and game_rating < 3799:
                        games['3400-3799'].append([game_id, game_rating, game['moves'], white, black, victory_status, winner])

                    elif game_rating > 3800 and game_rating < 4199:
                        games['3800-4199'].append([game_id, game_rating, game['moves'], white, black, victory_status, winner])

                    with open("LichessDataBase.txt", 'w') as f:  
                        # for key, value in games.items():  
                        #     f.write('%s:%s\n' % (key, value))
                        for k in games.keys():
                            f.write("'{}':'{}'\n".format(k, games[k]))
        
        except:
            pass

            


        
# 1000 - 1399, 1400 - 1799, 1800 - 2199, 2200 - 2599, 2600 - 2999, 3000 - 3399, 3400 - 3799