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

    @commands.command(name='info', help='Gives user info on their concurrent point status')
    async def info(self, ctx, *args):
        if not(args):
            response = usersDB.find({f'{ctx.author.id}': {'$exists': True}})
            if response.count() > 0:
                pass
                # display users data in an embed
            else:
                pass 
                # insert a new entry for the user, with his account balance
        else:
            pass

        await ctx.reply('ping', mention_author=False)

    async def generateEmbed(self, userData):
        # generate user embed 
        pass

    @commands.command(name='coinflip', help='Gives user info on their concurrent point status')
    async def coinflip(self, ctx, amount, flip):
        # coin flip gambling for virtual currency
        pass

    @commands.command(name='leaderboard', help='Shows the global leaderboard')
    async def leaderboard(self, ctx):
        # top 10 leaderboard
        pass

    @commands.command(name='donate', help='Donates points to another user')
    async def donate(self, ctx, receiver):
        # donation
        pass

    @commands.command(name='slots', help='Allows the user to play slots')
    async def slots(self, ctx, receiver):
        # allows you to play slots
        pass