import discord

from discord.ext import commands
from databaseClient import usersDB

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Used to test if the bot is functioning, responds with a pong')
    async def ping(self, ctx):
        await ctx.reply('pong', mention_author=False)

    @commands.command(name='pong', help='Used to test if the bot is functioning, responds with a pong')
    async def pong(self, ctx):
        await ctx.reply('ping', mention_author=False)