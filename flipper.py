import functions as f
import pygame
import requests
import pandas as pd
import time

# Initialise items dataframe
items_dataframe = f.initialise_items_dataframe()

# Wait for the API to update, then make the initial request
f.wait_for_update()
total_pages = f.initial_request()

# Asynchronously call all pages, then make dataframe
start = time.time()
auction_data = f.asyncio.run(f.main(total_pages))
auction_data = f.make_dataframe(auction_data)
end = time.time()
print("Async operation took " + str(round(end - start)) + " seconds.")

auction_data = auction_data.drop(['auctioneer', 'profile_id', 'coop', 'start', 'end', 'item_lore', 'extra', 'category', 'item_bytes', 'claimed', 'claimed_bidders', 'highest_bid_amount', 'last_updated','bin', 'bids', 'item_uuid'], axis=1)

def match_rows(name):
    # Filter rows in df1 where the 'name' column contains the name
    matches = auction_data[auction_data['item_name'].str.contains(name)]
    return matches.to_dict(orient='records')

items_dataframe['auctions'] = items_dataframe['name'].apply(match_rows)

to_drop = []
for name in items_dataframe['name']:
    matched_indices = auction_data[auction_data['item_name'].str.contains(name)].index
    to_drop.extend(matched_indices)
auction_data = auction_data.drop(to_drop)

auction_data.to_csv("CSVs/auction_data.csv")
items_dataframe.to_csv("CSVs/items.csv")

# Infinite loop
while True:

    # Wait for update
    f.wait_for_update()

    # Get new auctions and auctions ended in the last minute, and drop non-bin auctions
    auction_data, new_auctions, ended_auctions = f.get_updated_data(auction_data)

    # Print dataframe and save CSVs
    print(auction_data)
    auction_data.to_csv("CSVs/auction_data.csv")
    new_auctions.to_csv("CSVs/new_auctions.csv")
    ended_auctions.to_csv("CSVs/ended_auctions.csv")

    
    # items_to_remove = ['Minion I', 'Minion II', 'Minion III', 'Minion IV', 'Minion V', 'Minion VI', 'Minion VII', 'Minion VIII', 'Minion IX', 'Minion X', 'Minion XI' 'Minion XII']