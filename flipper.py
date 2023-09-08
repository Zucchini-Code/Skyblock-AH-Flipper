import pygame
import requests
import pandas as pd
import time

while True:
    auction_request = requests.get("https://api.hypixel.net/skyblock/auctions")
    time.sleep(5)
    auction_data = pd.DataFrame(auction_request.json()["auctions"])

    
    