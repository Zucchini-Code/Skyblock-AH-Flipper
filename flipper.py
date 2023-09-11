import pygame
import requests
import pandas as pd
import time
import datetime
import aiohttp
import asyncio


# Asynchronous function for getting a single page
async def get_page(session, url):
    async with session.get(url) as response:
        page = await response.json()
        print("Got Page: " + str(page['page'] + 1) + ", Time Updated: " + str(datetime.datetime.fromtimestamp(page["lastUpdated"]/1000)))
        return page['auctions']

# Asynchronously get all pages with aiohttp
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

# Initial request to get the time last updated and the total page count
initial_request = requests.get("https://api.hypixel.net/skyblock/auctions").json()
total_pages = initial_request["totalPages"]
update_time = datetime.datetime.fromtimestamp(initial_request["lastUpdated"]/1000)

# Asynchronously call all pages, then flatten list
auction_data = asyncio.run(main(total_pages))
auction_data = [item for sublist in auction_data for item in sublist]

# Make flattened list into dataframe and remove all non-bin
auction_data = pd.DataFrame(auction_data)
auction_data = auction_data.loc[auction_data.bin, :]

# Print dataframe
print(auction_data)

# End timing operation
end = time.time()
elapsed = end - start
print("Operation took " + str(elapsed) + " seconds")