import discord
from discord.ext import commands
from settings import *
from token_settings import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_author  = message.author
    message_details = message.content
    message_channel = message.channel

    print(f'{message_author} just sent a message in {message_channel}: {message_details}')

    if message.content.startswith('!hi'):
        print(message.content.startswith('!hello'))
        await message.channel.send('Hello!')

bot.run(token_id)


