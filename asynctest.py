import asyncio
import requests
import aiohttp


# Simple Sleep Example
# async def grabAPI(sec):
#     print("Start")
#     await asyncio.sleep(sec)
#     print("Done")

# async def getAllPages():
#     await asyncio.gather(*(grabAPI(i) for i in range(5)))

# print("a")
# asyncio.run(getAllPages())
# print("b")


# Example of why requests doesnt work
# async def grabAPI(page):
#     print(requests.get(f"https://api.hypixel.net/skyblock/auctions?page={page}").json()["page"])

# async def getAllPages():
#     await asyncio.gather(*(grabAPI(page) for page in range(10)))

# print("a")
# asyncio.run(getAllPages())
# print("b")


# Working example using AIOHTTP
async def grabAPI(page):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.hypixel.net/skyblock/auctions?page={page}") as response:
            checkPage = await response.json()
            print(checkPage["page"])
            return checkPage["page"]

async def getAllPages():
    pages = await asyncio.gather(*(grabAPI(page) for page in range(10)))
    return pages

print("a")
frog = asyncio.run(getAllPages())
print(frog)
print("b")