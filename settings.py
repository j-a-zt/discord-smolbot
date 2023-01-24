import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print('hi')
    print(str(message.content))
    if message.content.startswith('hi'):
        print(message.content.startswith('!hello'))
        await message.channel.send('Hello!')

bot.run('MTA2NzM2MDM5NDQyMDY5MDk0NA.GR8rFL.aC3hqaEiFnsOKeG1ma4QPuGGV66QcnCzxOpZXI')


