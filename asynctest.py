import asyncio
import requests
import aiohttp
import time


# # Requests Example
# async def grabAPI(page):
#     print(page)
#     return requests.get(f"https://api.hypixel.net/skyblock/auctions?page={page}").json()["auctions"]

# async def getAllPages(page_count):
#     await asyncio.gather(*(grabAPI(page) for page in range(page_count)))

# print("Start")
# start = time.time()

# asyncio.run(getAllPages(60))

# end = time.time()
# elapsed = end - start
# print("Operation took " + str(elapsed) + " seconds")



# # Old Example
# async def get_page(page_number):
#     print("Requesting Page: " + str(page_number + 1))
#     async with aiohttp.ClientSession() as session:
#         async with session.get(f"https://api.hypixel.net/skyblock/auctions?page={page_number}") as response:
#             page = await response.json()
#             print("Got Page: " + str(page["page"] + 1))
#             return page["auctions"]


# async def get_all_pages(total_pages):
#     auction_data = await asyncio.gather(*(get_page(page_number) for page_number in range(total_pages)))
#     return auction_data

# print("Start")
# start = time.time()

# auction_data = asyncio.run(get_all_pages(60))

# end = time.time()
# elapsed = end - start
# print("Operation took " + str(elapsed) + " seconds")




# # Youtube Example
# def get_tasks(session, total_pages):
#     tasks = []
#     for page_number in range(total_pages):
#         tasks.append(asyncio.create_task(session.get(f"https://api.hypixel.net/skyblock/auctions?page={page_number}")))
#     return tasks


# async def get_pages(total_pages):
#     auction_data = []
#     async with aiohttp.ClientSession() as session:
#         tasks = get_tasks(session, total_pages)
#         responses = await asyncio.gather(*tasks)
#         for response in responses:
#             auction_data.append(await response.json())
#     return auction_data

# print("Start")
# start = time.time()

# auction_data = asyncio.run(get_pages(60))

# end = time.time()
# elapsed = end - start
# print("Operation took " + str(elapsed) + " seconds")