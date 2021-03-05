import discord

from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Shows the help command')
    async def help(self, ctx):
        for cog in self.bot.cogs:
            print(self.bot.cogs[cog].__doc__)
