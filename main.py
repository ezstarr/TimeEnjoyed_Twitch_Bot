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
from count_database import trigger_a_count


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

        super().__init__(token, prefix='!', initial_channels=['timeenjoyed'])


    async def event_ready(self):
        """This function is an example of an event"""
        "Called once the bot goes online"
        # Notify someone when everything is ready
        # Is logged in and ready to use commands
        print(green(f'Logged in as | {self.nick}'))
        print(f'User id is | {self.user_id}')

    async def event_channel_joined(self, channel: twitchio.Channel):
        selected_greeting = random.choice(greetings)
        await channel.send(selected_greeting)
        # await channel.send("Hi guys. This is my lame draft greeting -_-. Ugh. Under construction")


    @commands.command()
    async def test(self, ctx: commands.Context):
        total = trigger_a_count()
        await ctx.send(f"TimeEnjoyed said test {total} times.")


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
    async def xkcd(self, ctx: commands.Context, comic_num):
        """Returns XKCD url and title."""
        int_comic_num = int(comic_num)
        comic_title = await xkcd.async_call(int_comic_num)
        await ctx.send(f'http://www.xkcd.com/{comic_num}/ - {comic_title}')


    @commands.command()
    async def shout_out(self, channel, ctx:commands.Context):
        """under construction"""
        global last_shoutout_Time
        if last_shoutout_Time == 0:
            timestamp()

    # nowtime = ((datetime.datetime.utcnow() - epoch).total_seconds()) - last_shoutout_Time
        # if nowtime > 60:
        #     timestamp()
        print(f'Shouted out {channel}')
        await ctx.send('BE SURE TO CHECK OUT https://twitch.tv/' + channel + " they are an awesome person")
        if channel in always_shoutout:
            await ctx.send('BE SURE TO CHECK OUT https://twitch.tv/' + channel + " they are an awesome person")


class Cooldown(commands.Cooldown):
    def __init__(self):
        self.ten_seconds = 10

    def cooldown_time(self):
        return self.ten_seconds


bot = TheTimeBot()
cooldown = Cooldown()

bot.run()


