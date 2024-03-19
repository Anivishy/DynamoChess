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

from chessdotcom import *
import webbrowser

import urllib.request

# async def gather_with_concurrency(n, *tasks):
#     semaphore = asyncio.Semaphore(n)
#     async def sem_task(task):
#         async with semaphore:
#             return await task
   
#     return await asyncio.gather(*(sem_task(task) for task in tasks))

urls = []
usernames = ["Hikaru"]
games = []
             
#, "MagnusCarlsen", "nihalsarin", "Firouzja2003", "Polish_fighter3000"]

Client.request_config["headers"]["User-Agent"] = (
    "asgasdf"
    "asgasdfsd"
)

async def post_async(username):
    response = get_player_game_archives(username)
    return response.__getattribute__('json')

async def fetch_async(url):
    with urllib.request.urlopen(url) as response:
        games.append(response)
        pprint(games)
        return
        #output = response.decode('utf-8')
    
async def main(usernames: list):
    async with aiohttp.ClientSession() as session:
        tasks = [post_async(username) for username in usernames]
        for coro in asyncio.as_completed(tasks):
            #results = await asyncio.gather(*tasks)
            result = await coro
            # with open("chessdotcom_urls.txt", 'w') as f:
            #     f.write(str(result['archives']))
            urls.append(result['archives'])

async def html_reader(urls):
    async with aiohttp.ClientSession() as session:
        urls = urls[-15:] 
        # ^^^ used to change how far back to go on a users data.
        #Increasing the value will go back further 1 month in time
        tasks = [fetch_async(url) for url in urls]
        for coro in asyncio.as_completed(tasks):
            result = await coro
            games.append(result)

    #pprint(results)

if __name__ == "__main__":
    while True:
        asyncio.run(main(usernames))
        #pprint(urls)
        usernames.clear()
        if len(urls) > 0:
            for url in urls:
                print("running")
                #for line in url:  
                asyncio.run(html_reader(url))                  
                for game in games:
                    #data = urlopen(game)
                    pprint(game)
                    pprint(game.read())
            urls.clear()