from twitchio.ext import commands
from dotenv import load_dotenv
import os

# Credentials
load_dotenv('.env')

client.run(os.environ['ACCESS_TOKEN'])

token = os.environ['ACCESS_TOKEN']

class Bot(commands.Bot):
    def __init__(self):
        # Initialize bot with access token, prefix, and a list of channels to join on boot.
        # prefix can be a callable, which returns a list of strings or a strings
        # initial_channels can also be callable
        super().__init__(token='TOKEN', prefix='?', initial_channels=['...'])

    async def event_ready(self):
        """This function is an example of an event"""
        # Notify someone when everything is ready
        # Is logged in and ready to use commands
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
    # If someone types ?hello, this command is invoked...
    # Send a hello back
    # Example of how to send a reply back
        await ctx.send(f'Hello {ctx.author.name}!')

bot = Bot()
bot.run()


