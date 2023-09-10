import aiohttp
import asyncio

async def get_page(session, url):
    async with session.get(url) as response:
        page = await response.json()
        print("Got Page " + str(page['page'] + 1))
        return page['auctions']

async def main(total_pages):
    async with aiohttp.ClientSession() as session:

        # Create list of tasks (different API calls)
        tasks = []
        for page_number in range(total_pages):
            url = f"https://api.hypixel.net/skyblock/auctions?page={page_number}"
            print("Requesting Page " + str(page_number + 1))
            tasks.append(asyncio.ensure_future(get_page(session, url)))

        # Then gather and return all responses as a list
        return await asyncio.gather(*tasks)

total_pages = 50
auction_data = asyncio.run(main(total_pages))