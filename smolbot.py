import discord
from discord.ext import commands
from token_settings import *
import mysql.connector
from datetime import datetime as dt
from settings import *

class SmolBot():
    def __init__(self):
        self.intents        = discord.Intents.all()
        self.discord_bot    = commands.Bot(command_prefix='!', intents=self.intents)
        self.token          = token_id

        ## Database
        self.db             = None
        self.cursor         = None
        self.connect_db() ## To make connection to DB

    def run_bot(self):
        @self.discord_bot.event
        async def on_message(message):

            if message.author == self.discord_bot.user: ## To ignore messages sent by bot
                return

            ## Store and log all the related details of the person sending the message
            message_author_name                     = message.author.name           ## Storing of message sender name in gamer tag
            message_author_discord_discriminator    = message.author.discriminator  ## Storing of message sender id in gamer tag
            message_author_discord_id               = message.author.id             ## Storing of message sender discord id
            message_id      = message.id                                            ## Storing ID of message sent
            message_details = message.content                                       ## Storing message content
            message_channel = message.channel.name                                  ## Storing channel where message was sent
            message_guild   = message.channel.guild.name                            ## Storing server where message was sent
            ## Handling to store message being replied to
            message_replyto = None                                                  ## Storing (if any) message ID of message being replied
            if message.reference is not None:
                message_replyto = message.reference.message_id

            print(f'{dt.now()} - {message_author_name}#{message_author_discord_discriminator} just sent a message in {message_channel}: {message_details:>5}')

            ## Insert message into DB user_message
            self.store_messages(
                user_name = message_author_name,                    ## Storing of message sender name in gamer tag
                user_tag = message_author_discord_discriminator,    ## Storing of message sender id in gamer tag
                user_discordID = message_author_discord_id ,        ## Storing of message sender discord id
                details=message_details,                            ## Storing message content
                channel=message_channel,                            ## Storing channel where message was sent
                message_id = message_id,                            ## Storing ID of message sent
                server = message_guild,                             ## Storing server where message was sent
                reply_to = message_replyto)                         ## Storing (if any) message ID of message being replied

            ## Set the name of the person to reply to
            ## Check if user has a nickname, then set to nickname. Else, set to Name in gamer tag
            if message.author.nick is not None:
                message_replyTo = message.author.nick
            else:
                message_replyTo = message_author_name

            ## Replying to Hello messages
            if message_details.startswith('$hello'):
                await message.reply(f'Hello {message_replyTo}')

        ## Run bot
        self.discord_bot.run(self.token)

    ## Function to make connection to DB
    def connect_db(self):
        try:
            self.db = mysql.connector.connect(
                host=db_creds['host'],
                user=db_creds['user'],
                passwd=db_creds['passwd'],
                database=db_creds['database'])
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            print(f'{dt.now()} - Failed to connect to database: {err}')

    ## Function to store messages by inserting row into DB
    def store_messages(self,user_name,user_tag,user_discordID,details,channel,message_id,server,reply_to,table='user_messages'):
        current_datetime = dt.now()

        if self.cursor is None: ## To check that there are current cursors to DB
            return

        try:
            self.cursor.execute(f'INSERT INTO {table} (CreateDateTime,User_Name,User_ID,User_Discord_ID,Channel,Message,Message_ID,Server,ReplyTo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (current_datetime,user_name,user_tag,user_discordID,channel,details,message_id,server,reply_to))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f'{current_datetime} - Failed to commit to database: {err}')
            return

        print(f'{current_datetime} - Message stored in {table}')

