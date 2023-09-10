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
        print("Got Page " + str(page['page'] + 1))
        return page['auctions']

async def main(total_pages):
    async with aiohttp.ClientSession() as session:

        # Create list of tasks (different API calls)
        tasks = []
        for page_number in range(total_pages):
            url = f"https://api.hypixel.net/skyblock/auctions?page={page_number}"
            print("Requesting Page " + str(page_number + 1))
            tasks.append(asyncio.ensure_future(get_page(session, url)))

        # Then gather and return all responses as a list
        return await asyncio.gather(*tasks)


start = time.time()
# total_pages = 50
total_pages = requests.get("https://api.hypixel.net/skyblock/auctions").json()["totalPages"]
print("Total Pages: " + str(total_pages))

auction_data = asyncio.run(main(total_pages))
# auction_data = [item for sublist in auction_data for item in sublist]
# auction_data = pd.DataFrame(auction_data)
# auction_data = auction_data.loc[auction_data.bin, :]
# print(auction_data)

end = time.time()
elapsed = end - start
print("Operation took " + str(elapsed) + " seconds")