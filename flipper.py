import pygame
import requests
import aiohttp
import numpy as np
import pandas as pd
import asyncio
import time



# Infinite loop of grabbing auctions. Repeats every 15 seconds.
while True:
    start = time.time()

    # Get the current number of total pages
    total_pages = requests.get("https://api.hypixel.net/skyblock/auctions").json()["totalPages"]
    print("Total Pages: " + str(total_pages))

    # Remove all auctions that aren't BIN auctions
    # auction_data = auction_data.loc[auction_data.bin, :]

    # print(auction_data)
    
    end = time.time()
    elapsed = end - start
    print("Operation took " + str(elapsed) + " seconds")
    time.sleep(15)