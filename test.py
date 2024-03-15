# import pytz
# import datetime

# tzs = pytz.all_timezones

# countries = pytz.country_timezones

# for t in tzs:
#     print(t)

# print("===")

import asyncio


async def returns_a_int() -> int:
    return 1


async def returns_None() -> None:
    return


async def main():
    
    my_int_task: asyncio.Task[int] = asyncio.create_task(returns_a_int())
    my_none_task: asyncio.Task[None] = asyncio.create_task(returns_None())
    
    print(my_int_task)
    

asyncio.run(main())