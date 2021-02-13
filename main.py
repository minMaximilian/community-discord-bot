import os

import discord
from discord.ext import commands
import host_commands
import fun_commands
from databaseClient import serversDB

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

if not(PREFIX):
    PREFIX="?"

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX))

@bot.event
async def on_guild_join(guild):
    if serversDB.find({str(guild.id): {'$exists': True}}).count() > 0: 
        pass
    else:
        payload = {str(guild.id): {}}
        serversDB.insert_one(payload)

@bot.event
async def on_ready():
    await start_up()

async def start_up():
    for guild in bot.guilds:
        if serversDB.find({str(guild.id): {'$exists': True}}).count() > 0: 
            pass
        else:
            payload = {str(guild.id): {}}
            serversDB.insert_one(payload)

# Adds different command modules to the bot
bot.add_cog(host_commands.Host(bot))
bot.add_cog(fun_commands.Fun(bot))

bot.run(TOKEN)
