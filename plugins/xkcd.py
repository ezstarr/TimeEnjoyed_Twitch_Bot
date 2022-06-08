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
        async_client.get_latest(),      # Comic object containing data of the latest xkcd comic
        async_client.get_random()       # Comic object of a random comic
        )
    print(
        responses[0],                   # async_client.get(100) output
        responses[0].title,
        responses[0].comic_url,
        sep='\n'
    )
    return responses[0].title

#
# async def get_title(comic_num):
#     responses = await asyncio.gather(
#         async_client.get(comic_num),  # Comic object with comic 100 data
#         async_client.get_latest(),  # Comic object containing data of the latest xkcd comic
#         async_client.get_random()  # Comic object of a random comic
#     )
#     return responses[0].title







#loop.run_until_complete(async_call(999))
