import discord

from discord.ext import commands

class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send('pong')