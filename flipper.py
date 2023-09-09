import pygame
import requests
import aiohttp
import numpy as np
import pandas as pd
import asyncio
import time


# Get individual page asynchronously using AIOHTTP
async def get_page(page_number):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.hypixel.net/skyblock/auctions?page={page_number}") as response:
            page = await response.json()
            print("Got Page " + str(page["page"] + 1))
            return page["auctions"]


# Use asyncio to "gather" all pages asynchrononously and return list
async def get_all_pages(total_pages):
    auction_data = await asyncio.gather(*(get_page(page_number) for page_number in range(total_pages - 1)))
    return auction_data


# Infinite loop of grabbing auctions. Repeats every 15 seconds.
while True:
    # Get the current number of total pages
    total_pages = requests.get("https://api.hypixel.net/skyblock/auctions").json()["totalPages"]
    print("Total Pages: " + str(total_pages))
    
    # Asynchronously grab all pages at once, and convert to pandas dataframe
    auction_data = pd.DataFrame(asyncio.run(get_all_pages(total_pages)))

    # Remove all auctions that aren't BIN auctions
    # auction_data = auction_data.loc[auction_data.bin, :]

    print(auction_data)
    time.sleep(15)