import pygame
import requests
import pandas as pd
import time
import datetime
import aiohttp
import asyncio
import python_nbt.nbt as nbt
import base64
import io

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
    auction_data = auction_data.drop(['auctioneer', 'profile_id', 'coop', 'start', 'end', 'item_lore', 'extra', 'category', 'claimed', 'claimed_bidders', 'highest_bid_amount', 'last_updated','bin', 'bids', 'item_uuid'], axis=1)
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
    print(f"Update Detected: Waited {round(waiting_timer_end - waiting_timer_start)} seconds")


# Initial request to get the time last updated and the total page count
def initial_request():
    initial_request = requests.get("https://api.hypixel.net/skyblock/auctions").json()
    total_pages = initial_request["totalPages"]
    print("Page Count: " + str(total_pages) + ". Last Updated: " + str(datetime.datetime.fromtimestamp(initial_request["lastUpdated"]/1000)))
    return total_pages

# Initialise list of items
def initialise_items_dataframe():
    items_dataframe = pd.DataFrame(requests.get("https://api.hypixel.net/resources/skyblock/items").json()["items"])[["name"]]
    items_dataframe.to_csv("CSVs/items.csv")
    items_dataframe['auctions'] = [[] for row in range(len(items_dataframe))]
    print("Items dataframe initialised!")
    return items_dataframe

# Update auction data with auctions created and deleted in the last minute
def get_updated_data(auction_data):
    # Get new auctions and auctions ended in the last minute, and drop non-bin auctions
    print("Getting new auction data...")
    new_auctions = pd.DataFrame(requests.get("https://api.hypixel.net/skyblock/auctions?page=0").json()["auctions"])
    ended_auctions = pd.DataFrame(requests.get("https://api.hypixel.net/skyblock/auctions_ended").json()["auctions"])
    new_auctions = new_auctions.loc[new_auctions.bin, :]
    new_auctions = new_auctions.drop(['auctioneer', 'profile_id', 'coop', 'start', 'end', 'item_lore', 'extra', 'category', 'claimed', 'claimed_bidders', 'highest_bid_amount', 'last_updated','bin', 'bids', 'item_uuid'], axis=1)
    ended_auctions = ended_auctions.loc[ended_auctions.bin, :]

    # Add in new auctions and remove dupes
    auction_data = pd.concat([new_auctions, auction_data])
    auction_data = auction_data.drop_duplicates(subset=["uuid"])

    # Remove ended auctions
    auction_data = auction_data[~auction_data['uuid'].isin(ended_auctions['auction_id'])]

    return auction_data, new_auctions, ended_auctions

def decode_inv_data(raw):
    decode = nbt.read_from_nbt_file(io.BytesIO(base64.b64decode(raw)))
    dict = nbt.NBTTagBase.json_obj(decode,full_json=False)
    return dict