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
            tasks.append(asyncio.ensure_future(get_page(session, url)))

        # Then gather and return all responses as a list
        print("Requesting Pages!")
        return await asyncio.gather(*tasks)


# Flatten list, convert to dataframe, and remove non-bin auctions
def make_dataframe(auction_data):
    auction_data = [item for sublist in auction_data for item in sublist]
    auction_data = pd.DataFrame(auction_data)
    auction_data = auction_data.loc[auction_data.bin, :]
    return auction_data


# Keep polling until the auction data gets updated
def wait_for_update():
    print("Waiting for update...")
    previous_timestamp = requests.get("https://api.hypixel.net/skyblock/auctions").json()["lastUpdated"]
    current_timestamp = previous_timestamp
    waiting_timer_start = time.time()
    while previous_timestamp == current_timestamp:
        current_timestamp = requests.get("https://api.hypixel.net/skyblock/auctions").json()["lastUpdated"]
    waiting_timer_end = time.time()
    print(f"Update Detected: Waited {waiting_timer_end - waiting_timer_start} seconds")


# Initial request to get the time last updated and the total page count
def initial_request():
    initial_request = requests.get("https://api.hypixel.net/skyblock/auctions").json()
    total_pages = initial_request["totalPages"]
    print("Page Count: " + str(total_pages) + ". Last Updated: " + str(datetime.datetime.fromtimestamp(initial_request["lastUpdated"]/1000)))
    return total_pages