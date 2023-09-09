import pygame
import requests
import aiohttp
import numpy as np
import pandas as pd
import asyncio
import time

# 
while True:
    auction_request = requests.get("https://api.hypixel.net/skyblock/auctions").json()

    auction_pages = auction_request["totalPages"]
    auction_data = auction_request["auctions"]
    
    for pages in range(1, auction_pages):
        auction_data += requests.get(f"https://api.hypixel.net/skyblock/auctions?page={pages}").json()["auctions"]
        print(f"Loading Pages: {pages}/{auction_pages - 1}")
    auction_data = pd.DataFrame(auction_data)
    auction_data = auction_data.loc[auction_data.bin, :]
    print(auction_data)
    time.sleep(30)