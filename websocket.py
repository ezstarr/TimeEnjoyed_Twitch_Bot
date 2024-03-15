import asyncio
import aiohttp
import json
from typing import Any

with open('wb-token.txt') as f:
    wbtoken = f.read()

queue = asyncio.Queue()

async def process_queue_items():
  while True:
      # Wait for an item to be available in the queue
      item = await queue.get()

      
      # Process the item (e.g., send it to the Bluetooth printer)
      # This is a placeholder for your actual processing logic
      print(f"Processing item: {item}")

      # then continue waiting.. forever.. because this loop will continue to wait for the next event
      

# Coroutine to handle WebSocket messages and put them into the queue
async def handle_websocket_messages(session):
  item_data: list[str | None] = []

  # sending a handshake to the server-bot (ws url), if it connects, server sends handshake back 
  async with session.ws_connect("wss://bot.timeenjoyed.dev/websockets/connect") as ws:
      
      # Next line is where client (this bot) subscribes to events in the serverbot
      # ws is a WebsocketClientResponse
      await ws.send_json({"op": "subscribe", "d": {"subscription": "eventsub"}})

      async for msg in ws:
          print(msg)
        
          data: dict[str, Any] = json.loads(msg.data)

          op_value = data["op"]
          print(f"op:  {op_value}")

          # if the operation received from the websocket is an event (1), get the event/subscription type.
          if op_value == 1:
            fake_data = "==this is fake data without being touched, just for testing=="

            # Extract "type" from the the data recevied from the websocket subscription, of twitch channel subscriptions
            subscription_type = data["d"]["data"]["subscription"]["type"]
            if subscription_type == "channel.channel_points_custom_reward_redemption.add":
                fake_data = "==========this is fake test data"
            if subscription_type == "channel.subscribe" or subscription_type == "channel.subscription.message":
                subscriber_id = data["d"]["data"]["event"]["user_id"]
                subscriber_name = data["d"]["data"]["event"]["user_name"]
                subscribe_tier = data["d"]["data"]["event"]["tier"]

                # if there's a message, grab the message
                if data["d"]["data"]["event"]["message"]:
                    subscriber_msg = data["d"]["data"]["event"]["message"]
                # item_data = [subscriber_id, subscriber_name, subscribe_tier]
                fake_data = ["timeenjoyed", "123"]
            await queue.put(fake_data)
      # op 0 - HELLO (handshake)
      # op 1 - EVENT (data for the event)
      # op 2 - NOTIFICATION (tells me everything except data for the event, and a type key which informs type of notification)
          
      # TODO: make sure it reconnects if it loses connection
          
      # TODO: if the msg has channel.subscribe in it.... 
          # get info about the subscriber 
          # create a asyncio.Queue to loop, and send the data through it.
            
async def main() -> None: 
    headers: dict[str, str] = {"Authorization": wbtoken}
    # create a queue to store the subscriber's information

    async with aiohttp.ClientSession(headers=headers) as session:
        asyncio.create_task(process_queue_items())
        await handle_websocket_messages(session)


        # TODO: send the information the printer via the loop.

asyncio.run(main())

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
                        "version":"1","condition":{"broadcaster_user_id":"410885037","reward_id":""},"transport":{"method":"webhook","callback":"https://bot.timeenjoyed.dev/eventsub/callback"},"created_at":"2023-11-23T06:06:45.775530268Z","cost":0},"event":{"broadcaster_user_id":"410885037","broadcaster_user_login":"timeenjoyed","broadcaster_user_name":"TimeEnjoyed","id":"180d03ab-7083-4daf-be1c-08cc7571e522","user_id":"1024780020","user_login":"rvynrgl2","user_name":"rvynrgl2","user_input":"https://www.youtube.com/watch?v=47HN6xOwphA","status":"unfulfilled","redeemed_at":"2024-03-08T01:14:27.983578746Z","reward":{"id":"1069c6b6-2fe4-4dec-8f21-6347ddf18b53","title":"Play this song","prompt":"Enter a song search or URL to play.","cost":1}}}}}', extra='')
"""