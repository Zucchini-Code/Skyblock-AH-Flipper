import functions as f
import pygame
import requests
import pandas as pd
import time

pd.DataFrame(requests.get("https://api.hypixel.net/resources/skyblock/items").json()["items"]).to_csv("CSVs/items.csv")
api_key = open("apikey.txt", "r").read()
pd.DataFrame(requests.get("https://api.hypixel.net/skyblock/auction?uuid=fbe3227298ba418793bc3c049c65c6c1",headers={"Api-Key":api_key}).json()["auctions"]).to_csv("CSVs/individual_item.csv")

# Wait for the API to update, then make the initial request
f.wait_for_update()
total_pages = f.initial_request()

# Asynchronously call all pages, then make dataframe
start = time.time()
auction_data = f.asyncio.run(f.main(total_pages))
auction_data = f.make_dataframe(auction_data)
end = time.time()
print("Async operation took " + str(round(end - start)) + " seconds.")

# Infinite loop
while True:

    # Wait for update
    f.wait_for_update()

    # Get new auctions and auctions ended in the last minute, and drop non-bin auctions
    print("Getting new auction data...")
    new_auctions = pd.DataFrame(requests.get("https://api.hypixel.net/skyblock/auctions?page=0").json()["auctions"])
    ended_auctions = pd.DataFrame(requests.get("https://api.hypixel.net/skyblock/auctions_ended").json()["auctions"])
    new_auctions = new_auctions.loc[new_auctions.bin, :]
    ended_auctions = ended_auctions.loc[ended_auctions.bin, :]

    # Add in new auctions and remove dupes
    auction_data = pd.concat([new_auctions, auction_data])
    auction_data = auction_data.drop_duplicates(subset=["uuid"])

    # Remove ended auctions
    auction_data = auction_data[~auction_data['uuid'].isin(ended_auctions['auction_id'])]

    # Print dataframe and save CSVs
    print(auction_data)
    auction_data.to_csv("CSVs/auction_data.csv")
    new_auctions.to_csv("CSVs/new_auctions.csv")
    ended_auctions.to_csv("CSVs/ended_auctions.csv")