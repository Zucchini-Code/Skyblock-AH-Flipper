import pygame
import requests
import pandas as pd
import time

# Start timing operation
start = time.time()

initial_request = requests.get("https://api.hypixel.net/skyblock/auctions").json()
total_pages = initial_request["totalPages"]
auction_data = initial_request["auctions"]

print("Total Pages: " + str(total_pages))
for page_number in range(1,total_pages):
    print(f"Getting Page {page_number + 1}/{total_pages}")
    auction_data += requests.get(f"https://api.hypixel.net/skyblock/auctions?page={page_number}").json()["auctions"]

auction_data = pd.DataFrame(auction_data)
auction_data = auction_data.loc[auction_data.bin, :]

print(auction_data)

end = time.time()
elapsed = end - start
print("Operation took " + str(elapsed) + " seconds")