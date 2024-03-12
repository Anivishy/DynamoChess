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

# async def gather_with_concurrency(n, *tasks):
#     semaphore = asyncio.Semaphore(n)
#     async def sem_task(task):
#         async with semaphore:
#             return await task
   
#     return await asyncio.gather(*(sem_task(task) for task in tasks))

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
        results = await asyncio.gather(*tasks)

    pprint(results)

if __name__ == "__main__":
    usernames = ["Hikaru", "MagnusCarlsen", "nihalsarin", "Firouzja2003", "Polish_fighter3000"]
    asyncio.run(main(usernames))