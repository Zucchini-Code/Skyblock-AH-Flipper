import asyncio
import requests
import aiohttp


# async def grabAPI(sec):
#     print("Start")
#     await asyncio.sleep(sec)
#     print("Done")

# async def getAllPages():
#     await asyncio.gather(*(grabAPI(i) for i in range(5)))

# print("a")
# asyncio.run(getAllPages())
# print("b")


# async def grabAPI(page):
#     print(requests.get(f"https://api.hypixel.net/skyblock/auctions?page={page}").json()["page"])

# async def getAllPages():
#     await asyncio.gather(*(grabAPI(page) for page in range(10)))

# print("a")
# asyncio.run(getAllPages())
# print("b")