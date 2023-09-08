import pygame
import requests
import pandas as pd
import time

while True:
    auction_data = requests.get("https://api.hypixel.net/skyblock/auctions")
    time.sleep(5)
    print(pd.DataFrame(auction_data.json()["auctions"]))

    
    