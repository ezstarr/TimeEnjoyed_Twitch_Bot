import asyncio.subprocess
from twitchio.ext import commands
from dotenv import load_dotenv
from simple_chalk import chalk, green
import datetime
import os
import logging
import twitchio
# import counter
import random
from plugins import tarotreading, xkcd
from count_database import trigger_a_count, return_test_number
# for sp recognition:
import threading
import speech_recognition as sr


# Opens .env file
load_dotenv('.env')

# Assigns secret access token to "token".
token = os.environ['ACCESS_TOKEN']

# Gets the "source paths"

# Logs events to help with future debugging and record keeping.
logging.basicConfig(level=logging.INFO)

# Helps keep track of time
epoch = datetime.datetime.utcfromtimestamp(0)
last_shoutout_Time = 0
always_shoutout = ['xmetrix']
bot_name = "TheTimeBot"
user_channel = 'timeenjoyed'

# ========= Open Greetings File ==================
greetings = []
greetings_file = open('data/landing-greetings.txt', 'r')
greeting_lines = greetings_file.readlines()

for line in greeting_lines:
    greetings.append(line)

greetings_file.close()

with open("data/landing-greetings.txt", "r") as greetings_file:
    greetings_file.readlines()

    print(greetings_file)

def timestamp():
    global last_shoutout_Time
    last_shoutout_Time = (datetime.datetime.utcnow() - epoch).total_seconds()


class TheTimeBot(commands.Bot):
    def __init__(self):
        # Initialize bot with access token, prefix, and a list of channels to join on boot.
        # prefix can be a callable, which returns a list of strings or a strings
        # initial_channels can also be callable

        super().__init__(token, prefix='!', initial_channels=[user_channel])
        self.sr_message_queue: asyncio.Queue = asyncio.Queue()
        SRThread(self).start()
        self.loop.create_task(self.sr_listen())


    async def event_ready(self):
        """This function is an example of an event"""
        "Called once the bot goes online"
        # Is logged in and ready to use commands
        print(green(f'Logged in as | {self.nick}'))
        print(f'User id is | {self.user_id}')

    async def event_channel_joined(self, channel: twitchio.Channel):
        selected_greeting = random.choice(greetings)
        await channel.send(selected_greeting)
        # await channel.send("Hi guys. This is my lame draft greeting -_-. Ugh. Under construction")

    async def sr_listen(self) -> None:
        await self.wait_for_ready()
        channel = self.get_channel(user_channel)
        while True:
            response = await self.sr_message_queue.get()
            if response['transcription'] is None:
                continue

            if 'time' in response['transcription']:
                print(response['transcription'])
                await channel.send('!time')

            if 'test' in response['transcription']:
                print(response['transcription'])
                await channel.send("!test")


    @commands.command()
    async def test(self, ctx: commands.Context):
        a_trigger = trigger_a_count()
        total = return_test_number()
        await ctx.send(f"TimeEnjoyed said test {total} times.")
        # total = trigger_a_count()
        # await ctx.send(f"Speech Recognition heard 'test' {total} times")

    @commands.command()
    async def soc(self, ctx: commands.Context):
        await ctx.send(f"https://www.instagram.com/time.enjoyed/ \nhttps://twitter.com/TimeEnjoyed_ \nhttps://github.com/ezstarr \nhttps://www.tiktok.com/@estherwlee \nhttps://discord.com/invite/xyJvutjuuY")
        # total = trigger_a_count()
        # await ctx.send(f"Speech Recognition heard 'test' {total} times")


    @commands.command()
    async def so3(self, ctx: commands.Context, channel):

        # If someone types ?hello, this command is invoked...
        # Send a hello back
        # Example of how to send a reply back
        await ctx.send('BE SURE TO CHECK OUT https://twitch.tv/' + channel + ' they are an awesome person')

    @commands.command()
    async def mbti(self, ctx:commands.Context):
        await ctx.send(f'https://www.16personalities.com/free-personality-test')


    @commands.command()
    async def getreading(self, ctx:commands.Context):
        tarot_choices = tarotreading.get_tarot_names_list()
        chosen_card = random.choice(tarot_choices)
        await ctx.send(f'{ctx.author.name}, your tarot card is {chosen_card}')


    @commands.command()
    async def xkcd(self, ctx: commands.Context, comic_num=""):
        """Returns XKCD url and title."""
        try:
            # get a valid comic_id:
            int_comic_num = int(comic_num)
            #comic_id = await xkcd.async_call(comic_num)
            xkcd_obj = await xkcd.async_call(int_comic_num)
            print(xkcd_obj)
            await ctx.send(f'{xkcd_obj.comic_url}/ - {xkcd_obj.title}')
                    # except int_comic_num == 0:
                    #     await ctx.send(
                    #         f"Here's the most recent comic (number is missing or out-of-range): http://www.xkcd.com/")
                    # except xkcd.xkcd_wrapper.exceptions.HttpError: #error for when comic is out of range
                    #     await ctx.send(
                    #         f"Here's the most recent comic (number is missing or out-of-range): http://www.xkcd.com/")
        except Exception as e:
            await ctx.send(f"Here's the most recent comic (number is missing or out-of-range): http://www.xkcd.com/")

    @commands.command()
    async def raid(self, ctx: commands.Context):
        await ctx.send(f"<3 Time To Enjoy The Raid <3 Time To Enjoy The Raid <3 Time To Enjoy The Raid <3 Time To Enjoy The Raid <3")

    @commands.command()
    async def raid1(self, ctx: commands.Context):
        await ctx.send(
            f"timeenRaid Time To Enjoy The Raid timeenRaid Time To Enjoy The Raid timeenRaid Time To Enjoy The Raid timeenRaid Time To Enjoy The Raid timeenRaid")

    @commands.command()
    async def raid2(self, ctx: commands.Context):
        await ctx.send(
            f"timeenRaid What is the raid message? timeenRaid What is the raid message? timeenRaid What is the raid message? timeenRaid What is the raid message? timeenRaid")

    @commands.command()
    async def bot_commands(self, ctx: commands.Context):
        await ctx.send(f"!getreading !xkcd [comic number]")


    # @commands.command()
    # async def so(self, channel, ctx:commands.Context):
    #     """under construction"""
    #     global last_shoutout_Time
    #     if last_shoutout_Time == 0:
    #         timestamp()

    # nowtime = ((datetime.datetime.utcnow() - epoch).total_seconds()) - last_shoutout_Time
        # if nowtime > 60:
        #     timestamp()
        # print(f'Shouted out {channel}')
        # await ctx.send('BE SURE TO CHECK OUT https://twitch.tv/' + channel + " they are an awesome person")
        # if channel in always_shoutout:
        #     await ctx.send('BE SURE TO CHECK OUT https://twitch.tv/' + channel + " they are an awesome person")


class Cooldown(commands.Cooldown):
    def __init__(self):
        self.ten_seconds = 10

    def cooldown_time(self):
        return self.ten_seconds


class SRThread(threading.Thread):

    def __init__(self, bot_):
        self.bot = bot_
        super().__init__(daemon=True)

    def run(self) -> None:
        recognizer = sr.Recognizer()
        microphone = sr. Microphone()

        if not isinstance(recognizer, sr. Recognizer):
            raise TypeError("'recognizer' must be 'Recognizer' instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("'microphone' must be 'Microphone' instance")

        while True:
            with microphone as source:
                while True:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                    response = {
                        "success" : True,
                        "error": None,
                        "transcription": None
                    }

                    try:
                        response["transcription"] = recognizer.recognize_google(audio)
                    except sr.RequestError:
                        # API was unreachable or unresponsive
                        response["success"] = False
                        response["error"] = "API unavailable"
                    except sr.UnknownValueError:
                        # speech was unintelligible
                        response["error"] = "Unable to recognize speech"
                    self.bot.loop.call_soon_threadsafe(self.bot.sr_message_queue.put_nowait, response)



bot = TheTimeBot()
cooldown = Cooldown()


print(__name__)

bot.run()


