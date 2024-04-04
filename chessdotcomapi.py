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
import aiohttp
import random
import concurrent.futures
import requests
import xmltojson
import chess
import re

from chessdotcom import *
import webbrowser

import urllib.request 
from urllib.request import urlopen
import http.client

# async def gather_with_concurrency(n, *tasks):
#     semaphore = asyncio.Semaphore(n)
#     async def sem_task(task):
#         async with semaphore:
#             return await task
   
#     return await asyncio.gather(*(sem_task(task) for task in tasks))

urls = []
unchecked_usernames = ["Hikaru"] #, "MagnusCarlsen", "nihalsarin", "Firouzja2003", "Polish_fighter3000"]
checked_usernames = []
games = []
active_fetch_threads = []
parsed_games = {'1000-1399': [],
                '1400-1799': [],
                '1800-2199': [],
                '2200-2599': [],
                '2600-2999': [],
                '3000-3399': [],
                '3400-3799': [],
                '3800-4199': []
                }
             
#, "MagnusCarlsen", "nihalsarin", "Firouzja2003", "Polish_fighter3000"]

Client.request_config["headers"]["User-Agent"] = (
    "asgasdf"
    "asgasdfsd"
)

async def post_async(username):
    response = get_player_game_archives(username)
    return response.__getattribute__('json')
    
async def main(usernames: list):
    async with aiohttp.ClientSession() as session:
        tasks = [post_async(username) for username in usernames]
        for coro in asyncio.as_completed(tasks):
            #results = await asyncio.gather(*tasks)
            result = await coro
            # with open("chessdotcom_urls.txt", 'w') as f:
            #     f.write(str(result['archives']))
            urls.append(result['archives'])

async def fetch_async(url):
    with urllib.request.urlopen(url) as response:
        games.append(response)
        pprint(games)
        return
        #output = response.decode('utf-8')

async def html_reader(urls):
    async with aiohttp.ClientSession() as session:
        urls = urls[-15:] 
        # ^^^ used to change how far back to go on a users data.
        #Increasing the value will go back further 1 month in time
        #pprint(urls)
        tasks = [fetch_async(url) for url in urls]
        for coro in asyncio.as_completed(tasks):
            result = await coro
            if result != None:
                games.append(result)

    #pprint(results)
                
def get_game_data():
    print("in get_game_data")
    threads = [threading.Thread(target= lambda: return_games(https_request)).start() for https_request in games]

    pprint(threads)


def return_games(https_request):
    print("in return_games")
    #webbrowser.open(https_request.url)
    game_data = json.loads(urlopen(https_request.url).read())['games'][0:1]
    #pgns = game_data['games'][0]
    #pprint(game_data)
    parse_games_tasking(game_data)
    #pprint(urllib.request.urlopen(https_request.url))    
    #pprint(xmltojson.parse(urllib.request.urlopen(https_request.url).read()))
    #pprint(requests.get(https_request.url))
    #pprint(data)

def parse_games_tasking(game_data):
    print("in parse_games_tasking")
    parse_threads = [threading.Thread(target= lambda: parse_games(game_info)).start() for game_info in game_data]

def parse_games(game_info):
    #Contains a List of Lists, format of each nested list: [game id, game elo, moves, whiteplayerinfo, blackplayerinfo]
    pprint(game_info)
    uuid = game_info['uuid']
    black = [game_info['black']['@id'], game_info['black']['rating'], game_info['black']['username'], game_info['black']['uuid']]
    white = [game_info['white']['@id'], game_info['white']['rating'], game_info['white']['username'], game_info['white']['uuid']]
    #0 = ID, 1 = rating, #2 = username, 3 = uuid
    if black[2] in checked_usernames:
        if white[2] not in checked_usernames:
            unchecked_usernames.append(white[2])
    else:
        unchecked_usernames.append(black[2])
    game_rating = (black[1] + white[1]) // 2
    #moves = chess.pgn.read_game(game_info['pgn'])
    moves = game_info['pgn']
    moves = moves[moves.index('1.'):]
    moves = moves[:moves.rfind('}') + 1]
    moves = re.sub("\{.*?\}","", moves)
    # i = 1
    # while "..." in moves:
    #     removal_string = str(i) + "..."
    #     moves.replace(removal_string, "")
    # i = 1
    game_details = [uuid, game_rating, moves, white, black]
    if game_rating > 1000 and game_rating < 1399:
        parsed_games['1000-1399'].append(game_details)

    elif game_rating > 1400 and game_rating < 1799:
        parsed_games['1400-1799'].append(game_details)

    elif game_rating > 1800 and game_rating < 2199:
        parsed_games['1800-2199'].append(game_details)

    elif game_rating > 2200 and game_rating < 2599:
        parsed_games['2200-2599'].append(game_details)

    elif game_rating > 2600 and game_rating < 2999:
        parsed_games['2600-2999'].append(game_details)

    elif game_rating > 3000 and game_rating < 3399:
        parsed_games['3000-3399'].append(game_details)

    elif game_rating > 3400 and game_rating < 3799:
        parsed_games['3400-3799'].append(game_details)

    elif game_rating > 3800 and game_rating < 4199:
        parsed_games['3800-4199'].append(game_details)

    with open("ChessDotComDataBase.txt", 'w') as f:  
        for k in parsed_games.keys():
            f.write("'{}':'{}'\n".format(k, parsed_games[k]))

    
if __name__ == "__main__":
    while True:
        asyncio.run(main(unchecked_usernames))
        #pprint(urls)
        for username in unchecked_usernames:
            checked_usernames.append(username)
        unchecked_usernames.clear()
        if len(urls) > 0:
            for url in urls:
                print("running")
                #for line in url:  
                asyncio.run(html_reader(url)) 
                t1 = threading.Thread(target= get_game_data)
                t1.start()
                active_fetch_threads.append(t1)
                t1.join()
                print("Loop Complete")
                #print(len(games))
                #pprint(games)                 
            urls.clear()