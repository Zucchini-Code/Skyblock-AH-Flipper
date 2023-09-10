import pygame
import requests
import pandas as pd
import time
import datetime
import aiohttp
import asyncio

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



# Start timing operation
start = time.time()

#this sends for the total number of pages in the auction list and runs the asyncronous stuff
initial_request = requests.get("https://api.hypixel.net/skyblock/auctions").json()
total_pages = initial_request["totalPages"]
update_time = initial_request["lastUpdated"]
auction_data = asyncio.run(main(total_pages)) #returns a list of list of dicts
auction_data = [item for sublist in auction_data for item in sublist]

#the below will have to change to get the data into a df
auction_data = pd.DataFrame(auction_data)
auction_data = auction_data.loc[auction_data.bin, :]

print(auction_data)

end = time.time()
elapsed = end - start
print("Operation took " + str(elapsed) + " seconds")