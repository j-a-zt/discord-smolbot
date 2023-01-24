import discord
from discord.ext import commands
from token_settings import *
import mysql.connector
from datetime import datetime as dt

class SmolBot():
    def __init__(self):
        self.intents        = discord.Intents.all()
        self.discord_bot    = commands.Bot(command_prefix='!', intents=self.intents)
        self.token          = token_id
        self.db = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'root',
            database = 'smolbot_messages'
        )
        self.cursor = self.db.cursor()

    def run_bot(self):
        @self.discord_bot.event
        async def on_message(message):

            if message.author == self.discord_bot.user:
                return

            message_author_name                     = message.author.name
            message_author_discord_discriminator    = message.author.discriminator
            message_author_discord_id               = message.author.id
            message_details = message.content
            message_channel = message.channel.name
            print(f'{dt.now()} - {message_author_name}#{message_author_discord_discriminator} just sent a message in {message_channel}: {message_details:>5}')
            self.store_messages(user_name = message_author_name,user_tag = message_author_discord_discriminator,user_discordID = message_author_discord_id ,details=message_details,channel=message_channel)

            if message_details.startswith('!hi'):
                print('asdasdasd')
                await message.channel.send('asdasd!')

        self.discord_bot.run(self.token)

    def store_messages(self,user_name,user_tag,user_discordID,details,channel):
        current_datetime = dt.now()
        table = 'user_messages'
        self.cursor.execute(f'INSERT INTO {table} (CreateDateTime,User_Name,User_ID,User_Discord_ID,Channel,Message) VALUES (%s,%s,%s,%s,%s,%s)', (current_datetime,user_name,user_tag,user_discordID,channel,details))
        self.db.commit()
        print(f'{current_datetime} - Message stored in {table}')

