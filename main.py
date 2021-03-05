import os

import discord
from discord.ext import commands
import host_commands
import fun_commands
import mod_commands
import help_command
from databaseClient import serversDB
import scheduling

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
    await load_scheduler()

async def start_up():
    for guild in bot.guilds:
        if serversDB.find({str(guild.id): {'$exists': True}}).count() > 0: 
            pass
        else:
            payload = {str(guild.id): {}}
            serversDB.insert_one(payload)

async def load_scheduler():
    x = serversDB.find()
    for l in x:
        for _, i in l.items():
            if isinstance(i, dict):
                for game, k in i.items():
                    for schedule in k['schedule']:
                        scheduling.schedule(schedule, game, list(l.keys())[1])

# Adds different command modules to the bot
bot.remove_command('help')
bot.add_cog(host_commands.Host(bot))
bot.add_cog(fun_commands.Fun(bot))
bot.add_cog(mod_commands.Mod(bot))
bot.add_cog(help_command.Help(bot))
bot.run(TOKEN)
