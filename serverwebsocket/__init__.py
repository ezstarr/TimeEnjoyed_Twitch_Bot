from __future__ import annotations

import asyncio
import aiohttp
import logging
import json
from PIL import Image
import sys
import twitchio
import io
from io import BytesIO

from typing import Any, TYPE_CHECKING
from plugins.printer import Printer

if TYPE_CHECKING:
    from typing_extensions import Self
    
    
logger: logging.Logger = logging.getLogger(__name__)


with open('wb-token.txt') as f:
    wbtoken = f.read()


# I added ... to the end of my comments (LOL Shut up copilot)
# Wait can you see my copilot? Oh you can't xD
class ServerSocket: 
    def __init__(self, uri: str, bot) -> None:  # You need to add a bot parameter here; We don't need uri I don't think since you hardcoded it xD

        self.session = None
        
        self.uri: str = 'wss://bot.timeenjoyed.dev/websockets/connect'  # or you could do uri: str = uri or 'wss://bot.timeenjoyed.dev/websockets/connect'; (uri: str | None = None) in the __init__ signature...
        self.ws: aiohttp.ClientWebSocketResponse | None = None

        # self.listen() starts running in the background (and is blocking)
        # self._runner IS a task or None.
        self._runner: asyncio.Task[None] | None = None
        self._processor: asyncio.Task[None] | None = None
        
        # Printer nonsense...
        self._printer_ping: asyncio.Task[None] | None = None
        self.processing: bool = False

        self.queue: asyncio.Queue = asyncio.Queue()
        self.printer = Printer(host="10:22:33:E1:2F:B7")
        self.pfp_img: Image
        self.bot = bot

    # opens the context manager
    async def __aenter__(self) -> Self:
        await self.connect()
        return self
    
    # exits context manager
    async def __aexit__(self, *_: Any) -> None: 
        await self.close()

    # connects to the server via websocket 
    async def connect(self) -> None:
        logger.info("Connecting to the server via websocket")
        
        await self.printer.connect()
        await asyncio.sleep(1)
        
        headers: dict[str, str] = {"Authorization": wbtoken}
        # opens a session connector and closes it too
        async with aiohttp.ClientSession(headers=headers) as session:
            # grabs a websocket connection
            self.ws = await session.ws_connect(self.uri)

            # detaches the session connector (without closing)
            self.session = session.detach() # store the detached session

        # create_task() schedules a task to be executed in the loop (from asyncio.run())
        # returns a scheduled TASK or NONE.
            
        # gets items from the queue and processes it in printer   
        self._processor = asyncio.create_task(self.process_queue_items())
        self._printer_ping = asyncio.create_task(self.ping_printer())

        # listens to websocket and puts heard data into queue
        self._runner = asyncio.create_task(self.listen())
        logger.info("Connected to the server via websocket")

    async def ping_printer(self) -> None:
        # Send a command to printer...
        count = 0
        
        while True:
            
            if not self.processing:
                try:
                    # await self.printer.get_FWDPI()
                    await self.printer.reset()
                except Exception as e:
                    count += 1
                    logger.warning(f"Failed to ping printer: {e}. Check the printer is connected.")
                else:
                    count = 0
            
            if count >= 5:
                # We can actually do reconnect logic here when we do the main listener reconnect logic as well..
                logger.error("Failed to ping printer too many times. Exiting printer ping task. Please reconnect.")
                break
            
            await asyncio.sleep(60)

    async def listen(self) -> None:
        """ Gets data from websocket and puts it into queue """
        assert self.ws is not None
        logger.info("Listening to the server via websocket")

        # subscribes to server websocket events
        await self.ws.send_json({"op": "subscribe", "d": {"subscription": "eventsub"}})

        # Technically you want to use a while loop here instead...
        # Don't worry about this today as this is fine for today...
        """
        while True:
            try:
                msg: aiohttp.WSMessage = await self.ws.receive()
            except aiohttp.ClientConnectionError:
                # reconnect here
                # We need to do the reconnect logic at some point
                return
            
            if msg.type == aiohttp.WSMsgType.CLOSED:
                # reconnect here
                # We need to do the reconnect logic at some point
                return
            
                # now we can process the data the same way we are curently are...

            # You need to cover all thewebsocket messages here too
            
            if op_value == 0:  # HELLO message
                # Do the thing...
            
            elif op_value == 1:  # EVENT
                # Do the thing...
                
            elif op_value == 2:  # NOTIFICATION; We can use to make sure we haven't been unsubbed; if we have resubscribe
                # Send the same JSON we send in listen to subscribe...
                
            else:
                # Log a info message or something...
        
        """
        async for msg in self.ws:
            data: dict[str, Any] = json.loads(msg.data)

            op_value: int = data["op"]
            print(f"op:  {op_value}")

            # if the operation received from the websocket is an event (1), get the event/subscription type.
            if op_value == 1:
                
                eventsub: dict[str, Any] = data["d"]["data"]
                event_type = eventsub["subscription"]["type"]

                if event_type == "channel.channel_points_custom_reward_redemption.add":
                    asyncio.create_task(self.process_redeem(eventsub))
                
                elif event_type == "channel.subscribe" \
                or event_type == "channel.subscription.message":
                    asyncio.create_task(self.process_subscription(eventsub))

    async def fetch_image_bytes(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status() # Ensure the request was successful
                image_bytes = await response.read()
                # print(image_bytes)
                fp: io.BytesIO = io.BytesIO(image_bytes)
                # ensures the next read operation/file pointer starts from beginning
                fp.seek(0)
                return fp
        
    async def process_redeem(self, eventsub):
        reward_name: str = eventsub["event"]["reward"]["title"]
        # TODO: PNG_REWARD: str = "PNG <-> FaceCam"
        
        if reward_name == "this does nothing":
            print("============================ A REDEEM")
            
            redeemer_id = int(eventsub["event"]["user_id"])

            print(f"redeemer_ int: {redeemer_id}")
            twitch_user_list: list[twitchio.User] = await self.bot.fetch_users(ids=[redeemer_id])
            logger.info(str(twitch_user_list))
            # url to profile pic:
            pfp_url = twitch_user_list[0].profile_image
            print(f" twitch user who made the redeem: {twitch_user_list}")


            self.pfp_img = await self.fetch_image_bytes(pfp_url)
            await self.queue.put(self.pfp_img)


    async def process_subscription(self, eventsub):
        # step 1: print subscriber's profile picture

        subscriber_id = int(eventsub["event"]["user_id"])
        subscriber_name = eventsub["event"]["user_name"]
        subscribe_tier = eventsub["event"]["tier"]

        twitch_user_list: list[twitchio.User] = await self.bot.fetch_users(ids=[subscriber_id])
        logger.info(str(twitch_user_list))
        pfp_url = twitch_user_list[0].profile_image

        # if there's a message, grab the message
        if eventsub["event"].get("message", None) is not None:
            subscriber_msg = eventsub["event"]["message"]

        # evenutally will be something like: item_data = [subscriber_id, subscriber_name, subscribe_tier]
        # for now, just printing pic, TODO: add message and generate PIL image
        self.pfp_img = await self.fetch_image_bytes(pfp_url)
        await self.queue.put(self.pfp_img)

                
    async def process_queue_items(self) -> None:
        # step 2: print subscriber's profile picture 
        """Takes items from the queue and sends it to the printer to be printed"""
        logger.info("Started queue processor for the printer")
        
        while True:
            # Wait for an item to be available in the queue
            item = await self.queue.get()
            
            # basic flag cause I am a basic biatch (mysty)
            self.processing = True # HERE
            
            try:
                await self.printer.print_image(item)
                print("tried to print")
            except Exception as e:
                logger.exception(e, exc_info=e)

            await asyncio.sleep(1)
            self.processing = False

            # then continue waiting.. forever.. because this loop will continue to wait for the next event
            # op 0 - HELLO (handshake)
            # op 1 - EVENT (data for the event)
            # op 2 - NOTIFICATION (tells me everything except data for the event, and a type key which informs type of notification)


"""
WSMessage(type=<WSMsgType.TEXT: 1>, 
          data='{
            "op":1,
            "d":{
                "event":"eventsub",
                "data":{
                    "subscription":{
                        "id":"21bc9b59-2fad-4d9e-b135-7f0f058bbeaa",
                        "status":"enabled",
                        "type":"channel.channel_points_custom_reward_redemption.add",
                        "version":"1",
                        "condition":{
                            "broadcaster_user_id":"410885037",
                            "reward_id":""},"transport":{"method":"webhook","callback":"https://bot.timeenjoyed.dev/eventsub/callback"},"created_at":"2023-11-23T06:06:45.775530268Z","cost":0},"event":{"broadcaster_user_id":"410885037","broadcaster_user_login":"timeenjoyed","broadcaster_user_name":"TimeEnjoyed","id":"180d03ab-7083-4daf-be1c-08cc7571e522","user_id":"1024780020","user_login":"rvynrgl2","user_name":"rvynrgl2","user_input":"https://www.youtube.com/watch?v=47HN6xOwphA","status":"unfulfilled","redeemed_at":"2024-03-08T01:14:27.983578746Z","reward":{"id":"1069c6b6-2fe4-4dec-8f21-6347ddf18b53","title":"Play this song","prompt":"Enter a song search or URL to play.","cost":1}}}}}', extra='')
"""