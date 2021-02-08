import os

import discord
from discord.ext import commands
import host_commands

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

if not(PREFIX):
    PREFIX="?"

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX))

# Adds different command modules to the bot
bot.add_cog(host_commands.Host(bot))

bot.run(TOKEN)
