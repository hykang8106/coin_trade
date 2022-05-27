import asyncio 

async def async_func1():
    print("Hello")

# this give error, so comment out
# async_func1() 
asyncio.run(async_func1())

""" loop = asyncio.get_event_loop()
loop.run_until_complete(async_func1())
loop.close() """
