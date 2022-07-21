import xkcd_wrapper, asyncio
import asyncio
from pathlib import Path


source_path = Path(__file__).resolve()
source_dir = source_path.parent
# This removes unimportant error messages from printing (windows):
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

loop = asyncio.new_event_loop()



async_client = xkcd_wrapper.AsyncClient()



async def async_call(c_num):
    responses = await asyncio.gather(
        async_client.get(c_num),          # Comic object with comic 100 data
        )
    print(responses)
    return responses[0]






# TODO: web scrape for titles in python, https://xkcd.com/archive/
"""
example dictionary to populate:

# create my own indices of titles and numbers, in my own database.

var = {{"id": "id", "title": "the title"},
       {"id": "id", "title": "the title"}}
"""



#loop.run_until_complete(async_call(999))
