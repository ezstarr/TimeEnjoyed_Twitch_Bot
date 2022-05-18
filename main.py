from twitchio.ext import commands
from dotenv import load_dotenv
from simple_chalk import chalk, green
import datetime
import os

# Credentials
load_dotenv('.env')

# client.run(os.environ['ACCESS_TOKEN'])

token = os.environ['ACCESS_TOKEN']

class Bot(commands.Bot):
    def __init__(self):
        # Initialize bot with access token, prefix, and a list of channels to join on boot.
        # prefix can be a callable, which returns a list of strings or a strings
        # initial_channels can also be callable
        super().__init__(token, prefix='!', initial_channels=['timeenjoyed'])

    async def event_ready(self):
        """This function is an example of an event"""
        # Notify someone when everything is ready
        # Is logged in and ready to use commands
        print(green(f'Logged in as | {self.nick}'))
        print(f'User id is | {self.user_id}')


    @commands.command()
    async def hello(self, ctx: commands.Context):
    # Example of how to send a reply back
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def test(self, ctx: commands.Context):
        # If someone types ?hello, this command is invoked...
        # Send a hello back
        # Example of how to send a reply back
        await ctx.send(f'how does this work {ctx.author.name}!')

    @commands.command()
    async def mbti(self, ctx:commands.Context):
        await ctx.send(f'https://www.16personalities.com/free-personality-test')

bot = Bot()
bot.run()


