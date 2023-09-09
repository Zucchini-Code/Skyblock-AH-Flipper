import asyncio
import time

# Simple Sleep Example
async def grabAPI(sec):
    print("Start")
    await asyncio.sleep(sec)
    print("Done")

async def getAllPages():
    await asyncio.gather(*(grabAPI(i) for i in range(6)))

print("Start")
start = time.time()

asyncio.run(getAllPages())

print("End")
end = time.time()
elapsed = end - start
print("Operation took " + str(elapsed) + " seconds")