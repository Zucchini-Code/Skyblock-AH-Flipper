import pygame
import requests
import aiohttp
import numpy as np
import pandas as pd
import asyncio
import time

async def get_page(session, url):
    async with session.get(url) as response:
        page = await response.json()
        print("Got Page " + str(page['page']))
        return page['auctions']

async def main():
    async with aiohttp.ClientSession() as session:

        # Create list of tasks (different API calls)
        tasks = []
        for page_number in range(total_pages):
            url = f"https://api.hypixel.net/skyblock/auctions?page={page_number}"
            tasks.append(asyncio.ensure_future(get_page(session, url)))

        # Then gather and return all responses as a list
        return await asyncio.gather(*tasks)

# Infinite loop of grabbing auctions. Repeats every 15 seconds.

start = time.time()

# Get the current number of total pages
# total_pages = requests.get("https://api.hypixel.net/skyblock/auctions").json()["totalPages"]
total_pages = 60
print("Total Pages: " + str(total_pages))

asyncio.run(main())

# Remove all auctions that aren't BIN auctions
# auction_data = auction_data.loc[auction_data.bin, :]

# print(auction_data)

end = time.time()
elapsed = end - start
print("Operation took " + str(elapsed) + " seconds")
time.sleep(15)