import pygame
import requests
import pandas as pd
import time

while True:
    auction_request = requests.get("https://api.hypixel.net/skyblock/auctions").json()

    auction_pages = auction_request["totalPages"]
    auction_number = auction_request["totalAuctions"]
    auction_data = auction_request["auctions"]

    for pages in range(1, auction_pages):
        auction_data += requests.get(f"https://api.hypixel.net/skyblock/auctions?page={pages}").json()["auctions"]
        print(f"Loading Pages: {pages}/{auction_pages}")
    auction_data = pd.DataFrame(auction_data)

    print(auction_data)
    time.sleep(30)