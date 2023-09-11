import functions as f
import pygame
import requests
import pandas as pd
import time

# Wait for the API to update, then make the initial request
f.wait_for_update()
total_pages = f.initial_request()

# Asynchronously call all pages, then flatten list
start = time.time()
auction_data = f.asyncio.run(f.main(total_pages))
auction_data = f.make_dataframe(auction_data)
end = time.time()
print("Async operation took " + round(end - start) + " seconds.")

# Infinite loop
while True:

    # Get auctions ended in the last minute
    ended = pd.DataFrame(requests.get("https://api.hypixel.net/skyblock/auctions_ended").json()["auctions"])

    # Print dataframe
    print(auction_data)

    # Then wait for update
    f.wait_for_update()