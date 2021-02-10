import os

import discord
from discord.ext import commands
import host_commands

import json

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

if not(PREFIX):
    PREFIX="?"

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX))


@bot.event
async def on_ready():
    await start_up()

# Ensures that each server has a json file for storage
# Using json files due to this being a private bot and scalability isn't a factor
# Upgrade to mongodb eventually
async def start_up():
    for guild in bot.guilds:
        file_name = str(guild.id) + ".json"
        
        data = {
        }

        if not(os.path.isfile(file_name)):
            with open(file_name, "w") as f:
                json.dump(data, f, indent=4)

# Adds different command modules to the bot
bot.add_cog(host_commands.Host(bot))

bot.run(TOKEN)
