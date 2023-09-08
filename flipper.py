import pygame
import requests
import json
import time

while True:
    auction_data = requests.get("https://api.hypixel.net/skyblock/auctions")
    time.sleep(5)
    print(auction_data.json())