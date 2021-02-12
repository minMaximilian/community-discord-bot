import os

import discord
from discord.ext import commands
import host_commands
from databaseClient import gamesDB

import json

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

if not(PREFIX):
    PREFIX="?"

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX))

@bot.event
async def on_guild_join(guild):
    if gamesDB.find({str(guild.id): {'$exists': True}}).count() > 0: 
        pass
    else:
        payload = {str(guild.id): {}}
        gamesDB.insert_one(payload)

@bot.event
async def on_ready():
    await start_up()

# Ensures that each server has a json file for storage
# Using json files due to this being a private bot and scalability isn't a factor
# Upgrade to mongodb eventually
async def start_up():
    for guild in bot.guilds:
        if gamesDB.find({str(guild.id): {'$exists': True}}).count() > 0: 
            pass
        else:
            payload = {str(guild.id): {}}
            gamesDB.insert_one(payload)

# Adds different command modules to the bot
bot.add_cog(host_commands.Host(bot))

bot.run(TOKEN)
