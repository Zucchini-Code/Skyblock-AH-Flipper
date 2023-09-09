import pygame
import requests
import aiohttp
import numpy as np
import pandas as pd
import asyncio
import time

# Define asynchronous functions to collect a large number of pages from API data in parallel
# Get individual pages asynchronously 
async def get_page(page):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.hypixel.net/skyblock/auctions?page={page}") as response:
            checkPage = await response.json()
            print(checkPage["page"])
            return checkPage["page"]

async def get_all_pages(total_pages):
    pages = await asyncio.gather(*(get_page(page) for page in range(total_pages)))
    return pages

while True:
    total_pages = requests.get("https://api.hypixel.net/skyblock/auctions").json()["totalPages"]

    total_pages = auction_request
    
    for pages in range(1, auction_pages):
        auction_data += requests.get(f"https://api.hypixel.net/skyblock/auctions?page={pages}").json()["auctions"]
        print(f"Loading Pages: {pages}/{auction_pages - 1}")
    auction_data = pd.DataFrame(auction_data)
    auction_data = auction_data.loc[auction_data.bin, :]
    print(auction_data)
    time.sleep(30)