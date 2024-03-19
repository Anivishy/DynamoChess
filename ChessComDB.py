import requests
import json
from pprint import pprint
import time
import io, base64
import os
import multiprocessing
import torch
import threading
from threading import Thread
import asyncio
import random
import concurrent.futures

from chessdotcom import *
import webbrowser

urls = []


        





















######################################################
                    ###OLD CODE###
######################################################
#from chessdotcom.aio import get_player_profile, Client
# Client.aio = True

# usernames = ["Hikaru"] 
# cors = [get_player_game_archives(name) for name in usernames]

# usernames = ["fabianocaruana", "GMHikaruOnTwitch", "MagnusCarlsen", "GarryKasparov"]

# cors = [get_player_profile(name) for name in usernames]

# async def gather_cors(cors):
#    responses = await asyncio.gather(*cors)
#    return responses

# responses = asyncio.run(gather_cors(cors))


# Client.request_config["headers"]["User-Agent"] = (
#     "asgasdf"
#     "asgasdfsd"
# )

# response = get_player_game_archives("Hikaru")
# pprint(response)

# response = response.__getattribute__('json')['archives'][0]

# pprint(response)


# data = {"archives"}
# json_archives = response[data]

# games = webbrowser.open(json_archives[0])
# pprint(games)

# url = 'https://api.chess.com/pub/player/{}/games/{}/{}/pgn'

# years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
# months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

# def get_games(user):
#     games_json = []
#     # for year in years:
#     #     for month in months:
#     seed_games = requests.get(url.format(user, 2023, 11),
#                             headers = {
#                                 'Content-Type': 'application/x-chess-pgn',
#                                 'Content-Disposition': 'attachment; filename="ChessCom_username_YYYYMM.pgn"'
#                             } 
#                 )    
#     games_json.append(seed_games)
#             # ndjson = seed_games.content.decode().split('\n')

#             # for json_obj in ndjson:
#             #     if json_obj:
#             #         games_json.append(json.loads(json_obj))

#     return games_json

# pprint(get_games('Hikaru'))